FROM jupyter/scipy-notebook:notebook-7.0.3
# reference https://github.com/jupyter/docker-stacks/blob/main/scipy-notebook/Dockerfile
# for libraries already installed via `mamba` 

USER root

RUN apt-get -y update
RUN apt-get -y install \
    gconf-service \
    libgl1-mesa-glx \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgconf-2-4 \
    libgdk-pixbuf-2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    wget \
    libcairo-gobject2 \
    libxinerama1 \
    libgtk2.0-0 \
    libpangoft2-1.0-0 \
    libthai0 \
    libpixman-1-0 \
    libxcb-render0 \
    libharfbuzz0b \
    libdatrie1 \
    libgraphite2-3 \
    libgbm1

USER $NB_UID

WORKDIR $HOME

# Install Python 3 packages using mamba, following convention from origin image
# RUN mamba install --quiet --yes \
#     'package-name'

# EPSCI - Canvas course ID: (https://canvas.harvard.edu/courses/110633)
RUN mamba install --quiet --yes \
    'cartopy'

# Install packages that can only be installed via pip
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

# Set up to enable save as webpdf
RUN pyppeteer-install
COPY jupyter_nbconvert_config.py ./.jupyter/
COPY jupyter_notebook_config.py ./.jupyter/

# Set workdir to home at the end of all tasks to ensure correct working dir
WORKDIR $HOME
