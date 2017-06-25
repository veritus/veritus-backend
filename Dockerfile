# Start with a python 3.6 image
FROM python:3.6

ENV PYTHONUNBUFFERED 1

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
