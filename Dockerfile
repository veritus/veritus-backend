# Start with a python 3 image
FROM python:3
ENV PYTHONUNBUFFERED 1

# Creates src folder in container
RUN mkdir /src
# Makes src dir the working directory
WORKDIR /src

# Install requirements
ADD requirements.txt /src/
RUN pip install -r requirements.txt

ADD . /src/