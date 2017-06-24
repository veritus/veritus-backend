# Start with a python 3 image
FROM python:3
ENV PYTHONUNBUFFERED 1

# Creates src folder in container
RUN mkdir /code

# Copy everything into the /code directory of the container
ADD . /code/

# Makes src dir the working directory
WORKDIR /code

# Install requirements
RUN pip install -r /code/requirements.txt
#RUN python3 src/manage.py migrate

#CMD ["python3", "src/manage.py", "migrate"]
#CMD ["python3", "src/manage.py", "loaddata", "init_data.json"]
#CMD ["python3", "src/manage.py", "runserver"]
