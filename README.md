# FAS OnDemand Jupyter Apps

This repository contains course-specific jupyter applications for Open OnDemand defined in a declarative configuration and programmatically generated. 

The [fas-ondemand-jupyter-app](https://github.com/fasrc/fas-ondemand-jupyter-app.git) repo is used as a base for all apps.

## Adding new apps

1. Add a new entry to `apps.json` (see examples).
2. Run the `update.py` script to create the app folder(s). 
3. _Optional_: Build and test the docker image locally.
4. Commit and push the changes.

Notes:
- Existing apps will not be modified by the process above. This merely bootstraps new apps from a template repo. They can be modified manually from that point. Or you can start over by deleting the app folder and running the update process again.
- The `form.yml` will need to be updated manually with the correct image for deployment to the RC academic cluster. This will only be known after the image has been built and pushed to docker hub.

## Github Actions

Github Actions will automatically build an image if the app is pushed and it contains a `Dockerfile`. Once published to docker hub at [harvardat](https://hub.docker.com/u/harvardat), it will be available to be pulled and converted to a singularity image on the RC academic cluster. 

## Building and testing docker images

To build and test a docker image locally:

```
$ export APP_NAME=fas-jupyter-demo
$ cd apps/$APP_NAME
$ docker build -t harvardat/$APP_NAME:latest .
$ docker run --rm -p 8888:8888 harvardat/$APP_NAME:latest
```

To manually tag and push a docker image:

```
$ export GIT_COMMIT_HASH=$(git log -1 --format=%h)
$ docker tag harvardat/$APP_NAME:latest harvardat/$APP_NAME:$GIT_COMMIT_HASH
$ docker push harvardat/$APP_NAME:$GIT_COMMIT_HASH
$ docker push harvardat/$APP_NAME:latest
```

To print a list of installed packages with conda or pip:

```
$ docker run --rm -it harvardat/$APP_NAME:latest /bin/bash -c "conda list"
$ docker run --rm -it harvardat/$APP_NAME:latest /bin/bash -c "pip list"
```

