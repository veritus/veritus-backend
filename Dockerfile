# Start with a python 3.6 image
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
RUN pylint **/*.py

# Cronjob setup
ADD docker/cronjob/crontab /etc/cron.d/crons

RUN chmod 0644 /etc/cron.d/crons

RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
