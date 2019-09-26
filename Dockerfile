FROM python:3.6.8

MAINTAINER Alef Delpino <alefdelpino@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime

RUN mkdir -p /dataproc && chmod -R 775 /dataproc

COPY requirements.txt /dataproc/requirements.txt

RUN pip install -U pip && pip install -r /dataproc/requirements.txt

COPY . /dataproc

WORKDIR /dataproc