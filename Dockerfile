FROM ubuntu:latest

#Autor
MAINTAINER Ramon Sanchez Garcia <chentaco@correo.ugr.es>

#Actualizar Sistema Base

RUN apt-get update && \
      apt-get -y install sudo

# Instalar Python
RUN sudo apt-get -y install python-setuptools
RUN sudo apt-get -y install python-dev
RUN sudo apt-get -y install build-essential
RUN sudo apt-get -y install python-psycopg2
RUN sudo apt-get -y install libpq-dev
RUN sudo apt-get -y install python-pip
RUN sudo pip install --upgrade pip

# Editor de textos en caso de necesitarlo

RUN sudo apt-get -y install nano

#Descargar aplicacion
RUN sudo apt-get -y install git
RUN sudo git clone https://github.com/Chentaco/Proyecto-IV.git

#Instalar aplicacion
RUN cd Proyecto-IV/ && pip install -r requirements.txt
RUN cd Proyecto-IV/ && python manage.py syncdb --noinput
RUN cd Proyecto-IV/ && python manage.py migrate

#Puerto
EXPOSE 8000
