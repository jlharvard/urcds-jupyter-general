FROM jupyter/minimal-notebook:notebook-6.5.1 AS build
# For specs reference https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-minimal-notebook

COPY src .

USER root

RUN apt-get update -y && apt-get -y install build-essential

RUN make install

FROM jupyter/minimal-notebook:notebook-6.5.1

COPY --from=build /usr/local/bin/fa /usr/local/bin
COPY --from=build /usr/local/bin/tournament /usr/local/bin

USER $NB_UID
WORKDIR $HOME
COPY --chown=$NB_UID:$NB_GID src/automata/* .
COPY --chown=$NB_UID:$NB_GID src/axelrod.prefs .

# Set workdir to home at the end of all tasks to ensure correct working dir
WORKDIR $HOME
