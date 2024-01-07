# Use an official Python runtime as a parent image
FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN     apt-get  update -y \
&& apt-get upgrade -y \
&& pip install --upgrade pip && pip install -r requirements.txt \
&& python manage.py makemigrations \
&& python manage.py migrate

COPY . /app/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
