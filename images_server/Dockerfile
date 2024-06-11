FROM ubuntu:latest
LABEL authors="Kaiffan"
MAINTAINER Pavel Baev 'pavel.baev44@gmail.com'

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y python3-pip python3-dev build-essential


FROM python:3.9-alpine
RUN pip install markupsafe==1.1.1 flask

COPY requirements.txt /images_server/requirements.txt
WORKDIR /images_server
COPY . /images_server

ENTRYPOINT ["python"]
CMD ["server.py"]