FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Install cron
RUN apt-get update && apt-get -y install cron

# Creates src folder in container
RUN mkdir /code

# Copy everything into the /code directory of the container
ADD . /code/

# Makes code dir the working directory
# and we change directory into it
WORKDIR /code

# Install requirements
RUN pip install -r requirements.txt

# Run linter
RUN pylint src/**

# Move crontab file to tmp as we need to add environment variables
# before adding them to /etc/cron.d/
ADD docker/cronjob/crontab /tmp/crons
# Create contab file and change permissions
RUN touch /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
# Create contab log file 
RUN touch /var/log/cron.log
