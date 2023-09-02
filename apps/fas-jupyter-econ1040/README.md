# FAS ECON 1040 Jupyter Image

This image is unusual in that it is not intended to use the majority of Jupyter features, but rather to use the Jupyter Notebook environment to provide students with access to a browser-based terminal environment where they can run some compiled binaries for a homework activity used in ECON 1040.

## Base image

This image is based on [jupyter/minimal-notebook](https://hub.docker.com/r/jupyter/minimal-notebook). There is a [guide on choosing between the available jupyter images](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-minimal-notebook), and this one is used because we don't need anything beyond basic Jupyter functionality.

## Activity code base

This build process relies on a code repository that must be cloned into the `src` folder from [Harvard-ATG/econ-1040-prisoners-dilemma](https://github.com/Harvard-ATG/econ-1040-prisoners-dilemma). The contents of the `src` folder are ignored by git.

## Building locally

To build the image, you can run this command from this repo
- `docker build -t fas-jupyter-econ1040 .`

After it's been built, these commands can be used for testing
- Full jupyter interface: `docker run -it -p 8888:8888 -e DOCKER_STACKS_JUPYTER_CMD=notebook fas-jupyter-econ1040`
- Bash only: `docker run -it fas-jupyter-econ1040 bash`

## OnDemand Configuration

The `form.yml` file needs to be configured so that the `jupyter_version` references the correct image, keeping in mind that the docker image must be pulled by academic cluster staff, converted to the [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/quick_start.html) image format, and made available to OnDemand in order to use it.

Here's the change that needs to be made in `form.yml`:

```yaml
---
title: Jupyter Notebook - ECON 1040
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
