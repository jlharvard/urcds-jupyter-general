FROM jupyter/tensorflow-notebook:tensorflow-2.11.0

# Eng Sci 201 requested by Demba Ba and the jupyter/tensorflow-notebook
# comes with scipy, numpy, matplotlib, pandas, sickit-learn, tensorflow, keras already, so we're just deriving from that base image.
#
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-tensorflow-notebook
#
# If the course requires any additional packages not already included,
# install them here.

# Install Python 3 packages using conda since pytorch errors out in mamba, following convention from origin image
RUN conda install --quiet --yes \
    'pytorch' \
    'torchvision'