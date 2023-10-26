FROM ubuntu:18.04

MAINTAINER buho_team "sistemas@buho.media"

ENV LAST_UPDATED 2021-09-09

ADD deploy.sh /

# Setup apt
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update

# Install required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq install -y -u python3 curl ghostscript imagemagick openssh-server wget libpq-dev python3-dev python-setuptools git-core python3-pip build-essential  python3-psycopg2

RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update

# Install required packages
RUN DEBIAN_FRONTEND=noninteractive sh deploy.sh requirements-docker


#upgrade de pip
RUN  pip3 install setuptools --upgrade
RUN pip3 install --upgrade pip
RUN pip3 install django-realtime --upgrade

RUN apt-get update -y
#RUN apt-get install -y tzdata

#UTF 8 Servidor
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ America/Bogota

#install requirements
ADD requirements.txt /verne_ramo/requirements.txt
RUN pip3 install -r /verne_ramo/requirements.txt --ignore-installed


WORKDIR /verne_ramo 
