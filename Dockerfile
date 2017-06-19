# Start with a python 3 image
FROM python:3
ENV PYTHONUNBUFFERED 1

# Creates src folder in container
RUN mkdir /code

# Copy contents of the /src directory into the /code directory of the container
ADD /src /code/
# Add requirements.txt to code directory
ADD requirements.txt /code/

# Makes src dir the working directory
WORKDIR /code

# Install requirements
RUN pip install -r /code/requirements.txt

CMD ["python3", "src/manage.py", "migrate"]
CMD ["python3", "src/manage.py", "loaddata", "init_data.json"]
CMD ["python3", "src/manage.py", "runserver"]