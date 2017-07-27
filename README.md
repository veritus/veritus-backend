[![Coverage Status](https://coveralls.io/repos/github/veritus/veritus-backend/badge.svg?branch=master)](https://coveralls.io/github/veritus/veritus-backend?branch=master)
[![Code Health](https://landscape.io/github/veritus/veritus-backend/master/landscape.svg?style=flat)](https://landscape.io/github/veritus/veritus-backend/master)

# Veritus backend

## Developing
Prerequisites are installing docker and docker-compose.

1. Run
```
$ docker-compose up
```
2. Open a browser at localhost:8000 and see the Django admin site
3. Make code changes
4. Rerun
```
$ docker-compose up
```
5. Voila your change has been added.

## Docker
The docker image here is NOT supposed to be run alone. As the backend requires a database, there is no use running it alone. Use docker-compose to run the backend and database together.

### Docker commands
#### Build image
Builds a local image of the project with the tag `latest`. 
```
docker build -t veritus/backend:latest .
```
This is automatically done by Docker Cloud in the build process and saved in the Docker image repository online.

#### Login to docker cloud
```
docker login
```
Input credentials.

#### Push image to docker cloud
You normally dont have to do this manually as the build process takes care of it.
```
docker push <IMAGE-NAME>:</TAG>
```
Example:
```
docker push veritus/backend:latest
```

### Docker compose
Docker compose can be used here to start the backend with a database. Simply run

```
$ docker-compose up
```

It also works to use this during development, as docker-compose mounts the source code directory into the docker container when run. Meaning you simply need to rerun 

```
docker-compose up
``` 
after making code changes.

## Sentry
### Setup
Run 
```
docker-compose run --rm web upgrade
```
to setup Sentry locally and creating a user. 

Run ```docker-compose up``` to start all the services and go to localhost:9000 to see sentry.
