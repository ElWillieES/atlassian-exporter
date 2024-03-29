FROM python:3.9.15-slim-bullseye

ENV TZ="Europe/Madrid"

RUN apt-get update && apt-get install -y git

RUN mkdir -p /usr/src/app
COPY app /usr/src/app/
COPY requirements.txt /usr/src/app/

WORKDIR /usr/src/app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
