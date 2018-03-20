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

### Make Migrations
When you are making changes to the data model, you have to generate the migration files

1. Run
```
docker-compose up
```
2. Then run, in another terminal window,
```
docker-compose exec backend python3 src/manage.py makemigrations 
```
3. Resolve anything Django asks you to resolve (non-nullable fields and such)
4. Migration file should not be generated in the correct domain!
5. Build the docker image again
```
docker build -t veritus/backend:latest .
```
6. Rerun and your changes should be live
```
docker-compose up
```

### Migrate
Sometimes you need to take some actions during the `migrate` command (you will see it in the console when running docker-compose).
Then simply run
```
docker-compose up
```
and then in another terminal window run
```
docker-compose exec backend python3 src/manage.py migrate 
```

### Run tests manually
To run tests manually then simply run
```
docker-compose up
```
and then in another terminal window run
```
docker-compose exec backend python3 src/manage.py test 
```

### Run pylint manually
To run tests manually then simply run
```
docker-compose up
```
and then in another terminal window run
```
docker-compose exec backend pylint src/**
```


### Run autopep8 manually
```
docker-compose up
```
and then in another terminal window run
```
docker-compose exec backend autopep8 --in-place --recursive . 
```

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

#### Connect to postgres using pgadmin
Run this to get the id of the docker container
```
$ docker ps
```
Then run this command to get the IP address of the container (should be close to the bottom)
```
$ docker inspect <id>
```

Then open pgAdmin
1. Click "Add a connection to a server" (claw at top)
2. Insert IP address you found out
3. Find the username and password in the docker-compose.yml file
4. Voila!

#### Run cron jobs in docker container
```
docker-compose exec backend python3 src/manage.py runcrons 
```
