# FAS BST 282 Jupyter Image

This image was customized for BST 282 with packages from [bioconda](https://bioconda.github.io/index.html).

## Base image

This image is based on [fas-jupyter-general](../fas-jupyter-general/Dockerfile), which in turn is based on `jupyter/scipy-notebook:notebook-6.5.2`. See [jupyter stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-minimal-notebook) for more details.

## Building locally

To build the image, you can run this command from this repo
- `docker build -t fas-jupyter-bst282 .`

After it's been built, these commands can be used for testing
- Full jupyter interface: `docker run -it -p 8888:8888 -e DOCKER_STACKS_JUPYTER_CMD=notebook fas-jupyter-bst282`
- Bash only: `docker run -it fas-jupyter-bst282 bash`


## Python module dependencies

See `environment.yml` for the full list of packages installed in this image (conda and pip).

To generate or update `environment.yml`:
- `docker run --rm <image name> conda env export -n base > environment.yml` 

## OnDemand Configuration

The `form.yml` file needs to be configured so that the `jupyter_version` references the correct image, keeping in mind that the docker image must be pulled by academic cluster staff, converted to the [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/quick_start.html) image format, and made available to OnDemand in order to use it.

Here's the change that needs to be made in `form.yml`:

```yaml
---
title: Jupyter Notebook - BST 282
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
