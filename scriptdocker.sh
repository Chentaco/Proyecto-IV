#!/bin/bash

# descargar repositorio de docker
sudo docker pull chentaco/mobagestor

# arrancar el contenedor
sudo docker run -i -t chentaco/mobagestor /bin/bash
