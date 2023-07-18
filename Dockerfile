FROM python:3.9-buster
WORKDIR /src

COPY requirements.txt /src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update

COPY . /src
