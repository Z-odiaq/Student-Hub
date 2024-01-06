# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN     apt-get  update -y \
&& apt-get upgrade -y \
&& apt-get install iputils-ping -y \
&& apt-get install net-tools -y \
&& pip install --upgrade pip && pip install -r requirements.txt \
&& python manage.py makemigrations \
&& python manage.py migrate 

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000
EXPOSE 22
# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
