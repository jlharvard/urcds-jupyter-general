#!/usr/bin/env python3


import json
import os
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.join(ROOT_DIR, 'apps')


def create_app(base, app):
    ''' 
    Creates the ondemand app folder. 
    If the app folder already exists, it will not overwrite it.
    '''
    dest = os.path.join(APPS_DIR, app['app_name'])
    if os.path.exists(dest):
        return False

    os.makedirs(dest)
    copy_base_repo(base, app)
    update_form_and_manifest(base, app)
    create_dockerfile(base, app)
    return True


def copy_base_repo(base, app):
    '''
    Copies the base ondemand app from a github repository.
    '''
    base_dir = os.path.join(ROOT_DIR, base['git_dir'])
    if not os.path.exists(base_dir):
        exec_shell(f"git clone --single-branch --branch {base['git_branch']} {base['git_url']} {base_dir}")

    app_dir = os.path.join(APPS_DIR, app['app_name'])
    for filename in ('form.yml.erb', 'manifest.yml.erb', 'submit.yml.erb', 'view.html.erb', 'template'):
        exec_shell(f"cp -R {base_dir}/{filename} {app_dir}/{filename}")


def update_form_and_manifest(base, app):
    '''
    Updates the form.yml and manifest.yml for the app.

    The assumption is that the base app has templates for these two files
    (i.e. form.yml.erb and manifest.yml.erb), and that we can update them 
    by applying ERB variables.
    
    Note that the "erb" CLI utility is part of the Ruby standard library,
    so you should have this if you have Ruby installed.
    '''
    app_type = base['app_type']
    app_dir = os.path.join(APPS_DIR, app['app_name'])
    title = app['title']
    docker_image = app.get('docker_image', base['docker_image'])

    memory = app.get("memory", {})
    memory_value = memory['value'] # required
    memory_select = memory.get('select', False)
    memory_min = memory.get('min')
    memory_max = memory.get('max')
    
    cpu = app.get("cpu", {})
    cpu_value = cpu['value'] # required
    cpu_select = cpu.get('select', False)
    cpu_min = cpu.get('min')
    cpu_max = cpu.get('max')

    # The OnDemand cluster uses Singularity for containers so the docker image
    # will ultimately be converted and turned into a SIF file. Our naming convention
    # is based on the existing dockerhub image name.
    singularity_filename = docker_image.replace('/', '_').replace(':', '_') + '.sif'

    # Prepare eRuby template vars 
    erb_vars = []
    erb_vars.append(f"@title = '{title}'")
    erb_vars.append(f"@{app_type}_version = '{singularity_filename}'")
    if memory_select:
        erb_vars.append(f"@custom_memory_per_node_select = true")
        erb_vars.append(f"@custom_memory_per_node_min = {memory_min}")
        erb_vars.append(f"@custom_memory_per_node_max = {memory_max}")
    erb_vars.append(f"@custom_memory_per_node = {memory_value}")
    if cpu_select:
        erb_vars.append(f"@custom_num_cores_select = true")
        erb_vars.append(f"@custom_num_cores_min = {cpu_min}")
        erb_vars.append(f"@custom_num_cores_max = {cpu_max}")
    erb_vars.append(f"@custom_num_cores = {cpu_value}")

    erb_vars_file = os.path.join(app_dir, 'vars.rb')
    with open(erb_vars_file, "w") as f:
        f.write("\n".join(erb_vars) + "\n")

    # Apply template vars 
    exec_shell(f"erb -r {erb_vars_file} {app_dir}/form.yml.erb > {app_dir}/form.yml")
    exec_shell(f"erb -r {erb_vars_file} {app_dir}/manifest.yml.erb > {app_dir}/manifest.yml")
    
    # Cleanup
    exec_shell(f"rm {app_dir}/form.yml.erb")
    exec_shell(f"rm {app_dir}/manifest.yml.erb")
    exec_shell(f"rm {erb_vars_file}")


def create_dockerfile(base, app):
    '''
    Creates a Dockerfile for the app with any specified packages added.
    Note that packages may be installed from CRAN, Github, or Bioconductor.
    ''' 
    app_type = base['app_type']
    if app_type == 'rstudio':
        create_rstudio_dockerfile(base, app)
    elif app_type == 'jupyter':
        create_jupyter_dockerfile(base, app)


def create_rstudio_dockerfile(base, app):
    ''' Creates rstudio dockerfile with additional packages. '''
    base_docker_image = base['docker_image']
    app_dir = os.path.join(APPS_DIR, app['app_name'])

    packages = app.get("packages", {})
    cran_packages = packages.get("cran", [])
    github_packages = packages.get("github", [])
    bioc_packages = packages.get("bioc", [])
    has_packages = len(cran_packages + github_packages + bioc_packages) > 0

    def charvector(packages):
        quoted_list = ",".join([f"\"{p}\"" for p in packages])
        return f"c({quoted_list})" if quoted_list else ""

    installs = []
    if len(cran_packages) > 0:
        installs.append("Rscript -e 'install.packages(%s)'" % charvector(cran_packages))
    if len(github_packages) > 0:
        installs.append("Rscript -e 'remotes::install_github(%s, build_vignettes=TRUE)'" % charvector(github_packages))
    if len(bioc_packages) > 0:
        installs.append("Rscript -e 'BiocManager::install(%s, ask=False)'" % charvector(bioc_packages))

    instructions = [f"FROM {base_docker_image}"]
    instructions.append("RUN " + " \\\n\t&& ".join(installs))

    if has_packages:
        with open(os.path.join(app_dir, "Dockerfile"), "w") as f:
            f.write("\n".join(instructions))


def create_jupyter_dockerfile(base, app):
    ''' Creates jupyter dockerfile with additional packages. '''
    base_docker_image = base['docker_image']
    app_dir = os.path.join(APPS_DIR, app['app_name'])

    packages = app.get("packages", {})
    pip_packages = packages.get("pip", [])
    conda_packages = packages.get("conda", [])
    conda_channels = packages.get("channels", [])
    has_packages = len(pip_packages + conda_packages) > 0

    instructions = [f"FROM {base_docker_image}"]
    if len(pip_packages) > 0:
        instructions.append("RUN pip install --no-cache-dir {}".format(" ".join(pip_packages)))
    if len(conda_channels) > 0:
        instructions.append("RUN conda config --append channels {}".format(" ".join(conda_channels)))
    if len(conda_packages) > 0:
        instructions.append("RUN conda install --quiet --yes {}".format(" ".join(conda_packages)))

    if has_packages:
        with open(os.path.join(app_dir, "Dockerfile"), "w") as f:
            f.write("\n".join(instructions))


def exec_shell(cmd):
    ''' Execute a shell command. '''
    subprocess.check_call(cmd, shell=True)


def load_apps():
    ''' Loads JSON file that defines the app configurations. '''
    data = None
    with open(os.path.join(ROOT_DIR, 'apps.json'), 'r') as f:
        data = json.load(f)
    
    # quick sanity check
    for key in ('app_type', 'git_url', 'git_dir', 'git_branch', 'docker_image'):
        assert key in data['base'], f"Base missing required attribute: {key}"
    for i, app in enumerate(data['apps']):
        for key in ('app_name', 'title', 'cpu', 'memory'):
            assert key in app, f"App {i} is missing required attribute: {key} {app}"

    return data


def main():
    data = load_apps()
    for app in data['apps']:
        created = create_app(data['base'], app)
        if created:
            print(f"Created {app['app_name']}")
        else:
            print(f"Skipped {app['app_name']} -- already created")


if __name__ == "__main__":
    main()
