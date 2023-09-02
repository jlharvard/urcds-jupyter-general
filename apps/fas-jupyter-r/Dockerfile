FROM jupyter/r-notebook:r-4.1.3

# For details on the base image:
#   https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-r-notebook
#
# Install additional packages here.

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
    libgbm1 \
    gnupg

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

USER $NB_UID

RUN pyppeteer-install
COPY jupyter_nbconvert_config.py ./.jupyter/
COPY jupyter_notebook_config.py ./.jupyter/

WORKDIR $HOME

