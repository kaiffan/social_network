FROM ubuntu:latest
LABEL authors="Kaiffan"
MAINTAINER Pavel Baev 'pavel.baev44@gmail.com'

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y python3-pip python3-dev build-essential


FROM python:3.10-slim

WORKDIR /social-network
COPY ../social_network /social-network

COPY requirements.txt /social-network/
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]