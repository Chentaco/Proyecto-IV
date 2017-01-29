#!/bin/bash
#Herramientas necesarias
sudo apt-get update
sudo apt-get install nodejs-legacy
sudo apt-get install npm
sudo npm install -g azure-cli
sudo pip install paramiko PyYAML jinja2 httplib2 ansible
sudo wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_x86_64.deb
sudo dpkg -i vagrant_1.8.1_x86_64.deb
vagrant plugin install vagrant-azure

#Despliegue en Azure
cd ../deployAzure/
export ANSIBLE_HOSTS=~/ansible_hosts


#Despliegue de la app
fab -p 'chentaco' -H vagrant@mobagestor.cloudapp.net ejecutar_app
