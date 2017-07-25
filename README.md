[![Build Status](https://travis-ci.org/veritus/veritus-backend.svg?branch=master)](https://travis-ci.org/veritus/veritus-backend)
[![Coverage Status](https://coveralls.io/repos/github/veritus/veritus-backend/badge.svg?branch=master)](https://coveralls.io/github/veritus/veritus-backend?branch=master)
[![Code Health](https://landscape.io/github/veritus/veritus-backend/master/landscape.svg?style=flat)](https://landscape.io/github/veritus/veritus-backend/master)

# Politech-backend

## Recommended tools
1. [Pycharm](https://www.jetbrains.com/pycharm/): Very good python IDE
2. [Pgadmin3](http://www.pgadmin.org/): Very comfortable GUI for postgresql
3. [Postman](http://www.getpostman.com/): Great chrome app for testing the REST API
4. Ubuntu / Mac (That's what we are using!)

## Initial setup
1. Install **PostgreSQL** with your favourite package installer
`sudo aptitude install postgresql postgresql-contrib`
2. Download [virtualenv](https://pypi.python.org/pypi/virtualenv)
3. Create a virtual env in the project directory (politech_backend) called env
`virtualenv -p python3.6 env`
4. Start your virtual environment
`source env/bin/activate`
5. Install required dependencies in requirements.txt with pip
`pip install -r requirements.txt`

## Developing
1. Set DB_USER and DB_PASS as environmental variables after starting the virtual environment
f.x
`export DB_USER=<Postgres username>`
`export DB_PASS=<Postgres password>`
2. Try running the server (might not run if you have not setup the database yet)
`python manage.py runserver`

## Create politech user in postgres
1. Run this command to switch to postgres default user
`sudo su - postgres`
2. Create a new user called politech
`createuser -P -s -e politech`
3. Then you will be asked to provide a password. Just press enter.
4. You have just created a new user in postgres. Very nice!

## Create server in pgadmin3
1. Download [pgadmin3](https://www.pgadmin.org/download/) - Great GUI tool for postgres.
2. Click add server
3. Fill in the information needed (name (I used politech), host, port, username, password) -
That information can be found in the settings.py file.

## Create database in pgadmin3
1. Click the newly created server.
2. Right click "Databases" and create one called 'politech' with the owner being the politech user we created earlier.
3. Run the django server = Should detect the database you just created.

## Migration
After adding a new model or making a change in the model you should
1. Make a migration
`python manage.py makemigrations`
2. Migrate those migrations
`python manage.py migrate`
3. Now your changes should be in the postgres database

## Run tests
`python manage.py test`

## Code review process
1. Checkout branch via git
2. run tests
`python manage.py test`
3. Perform manual testing of new feature
4. Read newly commited code and make sure its up to expectations
5. Accept pull request on github if you are happy with the code additions

## Installing a new package via pip
1. Start virtual environment
`source env/bin/activate`
2. Install package
`pip install <PACKAGE NAME>`
3. Add to requirements.txt
`pip freeze > requirements.txt`

## Cron jobs
1. Open crontab
`crontab -e
2. Add cronscript. For Ari on Ubuntu this worked:
`SHELL=/bin/bash */5 * * * * cd home/path/to/project/directory source env/bin/activate && python manage.py runcrons
3. Write correct path

# Docker
The docker image here is NOT suppose to be run alone. As the backend requires a database, there is no use running it alone. Use docker-compose to run the backend and database together.

## Docker commands
### Build image
Builds a local image of the project with the tag ```latest```. 
```
docker build -t veritus/backend:latest .
```
This is automatically done by Docker Cloud in the build process and saved in the Docker image repository online.

###Login to docker cloud
```
docker login
```
Input credentials.

###Push image to docker cloud
You normally dont have to do this manually as the build process takes care of it.
```
docker push <IMAGE-NAME>:</TAG>
```
Example:
```
docker push veritus/backend:latest
```

## Docker compose
Docker compose can be used here to start the backend with a database. Simply run

```
$ docker-compose up
```

It also works to use this during development, as docker-compose mounts the source code directory into the docker container when run. Meaning you simply need to rerun ```docker-compose up``` after making code changes.
