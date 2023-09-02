# FAS Python Jupyter Notebook R Kernel Image

This is the image for using an R kernel in Jupyter Notebook in FAS OnDemand. It's intended to meet the needs of most data science and research workflows without introducing compatibility issues.

## Base image

This image is based on [jupyter/r-notebook](https://hub.docker.com/r/jupyter/r-notebook). There is a [guide on choosing between the available jupyter images](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook), and this one is used because it has the R kernel pre-installed, along with the most commonly used libraries for data science in R.

## Installed packages

There currently aren't any additional R packages installed beyond what's included in the initial image. The `packages.txt` file contains a list of the packages installed along with their versions for reference when checking for new dependencies in new OnDemand requests. It is created by running `docker run --rm <image name> Rscript -e "as.data.frame(installed.packages()[,c(1,3)])" > packages.txt` after building a new image locally.

## Notebook config files

The two config files in this folder are copied into the `.jupyter` folder in the home directory for the jupyter notebook user. Currently they just have a setting to disable chromium sandboxing, used in downloading PDFs via HTML in Jupyter Notebook, but other modifications to notebook and/or nbconvert behavior can be added there.

* [Notebook config options](https://jupyter-notebook.readthedocs.io/en/stable/config.html)
* [Nbconvert config options](https://nbconvert.readthedocs.io/en/latest/config_options.html)
