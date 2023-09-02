# FAS Python Jupyter Notebook General Image

This is the default image for Python/Jupyter in FAS OnDemand. It's intended to meet the needs of most data science and research workflows without introducing compatibility issues. If a library is requested during a term and can be added to this repo without conflict, then it should be.

## Base image

This image is based on [jupyter/scipy-notebook](https://hub.docker.com/r/jupyter/scipy-notebook). There is a [guide on choosing between the available jupyter images](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook), and this one is used because it has the most commonly requested Python libraries already installed.

## Python module dependencies

Dependencies are specified in `requirements.in` and then compiled with `pip-compile` from [piptools](https://github.com/jazzband/pip-tools) into the `requirements.txt` file, which allows us to keep track of which versions of which libraries are installed. Any dependencies that can't be installed via pip can be installed by their preferred method in the Dockerfile.

A full list of the Python libraries available can be found in `environment.yml` in this folder. It has a list of everything installed on this image, regardless of how it was installed (in theory, I'm sure it's possible to go around conda and pip).

When developing, generate a new `environment.yml` file locally from the new docker image with `docker run --rm <image name> conda env export -n base > environment.yml` from this directory.

## Notebook config files

The two config files in this folder are copied into the `.jupyter` folder in the home directory for the jupyter notebook user. Currently they just have a setting to disable chromium sandboxing, used in downloading PDFs via HTML in Jupyter Notebook, but other modifications to notebook and/or nbconvert behavior can be added there.

* [Notebook config options](https://jupyter-notebook.readthedocs.io/en/stable/config.html)
* [Nbconvert config options](https://nbconvert.readthedocs.io/en/latest/config_options.html)

## Building locally

To build the image, you can run this command from this repo
- `docker build -t fas-jupyter-cs109a .`

After it's been built, this command will start it for testing
- `docker run -it -p 8888:8888 -e DOCKER_STACKS_JUPYTER_CMD=notebook fas-jupyter-cs109a`

## OnDemand Configuration

The `form.yml` file needs to be configured so that the `jupyter_version` references the correct image, keeping in mind that the docker image must be pulled by academic cluster staff, converted to the [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/quick_start.html) image format, and made available to OnDemand in order to use it.

Here's the change that needs to be made in `form.yml`:

```yaml
---
title: Jupyter Notebook - CS 109a
cluster: "academic"
attributes:
  rstudio_version: "imagename.sif"  # <-- Change Me
```

The naming convention we've adopted for converting docker images to singularity files (`.sif`) is as follows:

```
user/repo:tag -> user_repo_tag.sif
```

For example:

```
harvardat/fas-jupyter-general:sha-7b5663a -> harvardat_fas-jupyter-general_sha-7b5663a.sif
```

Note that the `form.yml` can be updated before the image is pulled to the cluster, but just be aware that the server won't launch successfully until the image is actually available in the cluster.
