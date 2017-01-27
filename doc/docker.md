#Entorno de pruebas
Lo primero ha sido preparar la imagen con la aplicación y sus dependencias instaladas para que la ejecución de TusPachangas sea posible. Esto lo he realizado mediante un fichero **Dockerfile**, el cual puede consultarse en este repositorio en la carpeta raíz. En este fichero se especifican las acciones a realizar para preparar la imagen. En mi caso, le indico que se base en una imagen Ubuntu oficial, que actualice los repositorios, que instale algunos paquetes necesarios de Python, se descargue el repositorio de TusPachangas, instale las dependencias de la aplicación en sí, y realice las migraciones de bases de datos necesarias.

Una vez creado dicho fichero, hay que unir la cuenta de DockerHub con la de GitHub.
![linkGitHubDockerHub](http://i1016.photobucket.com/albums/af281/raperaco/linkGitHubDockerHub_zpsbe8n1l2k.png)

Tras esto, pulsamos en **Create** y después en **Automated Build** y seleccionamos el repositorio de nuestra aplicación. Tras esto, nos aparecerán los ajustes que tendrá la construcción automática en la que escribimos una breve descripción de la imagen que crearemos.
![automatedBuild](http://i1016.photobucket.com/albums/af281/raperaco/automatedBuild_zpshybcr5pu.png)

Tras pulsar en Create, falta indicarle que se automatizará la construcción a partir de push sobre la rama. Hay que pulsar en el botón Trigger en el menú Building Settings (también se podría haber hecho en el proceso de creación):
![triggerPushDocker](http://i1016.photobucket.com/albums/af281/raperaco/triggerPushDocker_zpsihdttbzp.png)

Mencionar que tras cada cambio que se realice en el repositorio es integrado en la imagen de DockerHub.

La página en DockerHub referente a mi imagen se puede encontrar [aquí](https://hub.docker.com/r/mabarrbai/tuspachangas/)

Para **descargar** la imagen:
~~~
sudo docker pull mabarrbai/tuspachangas
~~~

Para **iniciarla y ejecutar la aplicación TusPachangas**:
~~~
sudo docker run -i -t mabarrbai/tuspachangas /bin/bash
cd /TusPachangas/
python manage.py runserver 0.0.0.0:5500 &
~~~

Ya sólo falta saber la IP de dicho contenedor con el comando **ifconfig**.

Para **automatizar** todo este proceso, he creado un **script docker.sh** el cual se puede encontrar en la carpeta /scripts del repositorio TusPachangas.
~~~
#!/bin/bash

#Descargar docker
sudo wget -qO- https://get.docker.com/ | sh
# Iniciar el servicio docker
sudo service docker start
#Descargar la imagen
sudo docker pull mabarrbai/tuspachangas
#Ejecutar la imagen
sudo docker run -i -t mabarrbai/tuspachangas /bin/bash 
~~~

Tras ejecutarlo con **./docker.sh**, este script inicia el contenedor y nos mete en un terminal de dicho contenedor. Ahora sólo faltaría ejecutar la aplicación TusPachangas:
~~~
cd TusPachangas/
python manage.py runserver 0.0.0.0:5500 &
~~~

De esta forma está escuchando en el puerto 5500 aunque podría elegirse otro cualquiera de los libres.

Ya sólo quedaría saber cual es la IP de dicho container, lo vemos con **ifconfig**.
![ifconfigContainer](http://i1016.photobucket.com/albums/af281/raperaco/ifconfigContainer_zpsdfuwlmvp.png)

Vemos que es la 172.17.0.2. 
Ahora en un navegador, introducimos dicha IP seguida del puerto especificado, en mi caso 5500 y vemos la aplicación en ejecución:
![appContainer](http://i1016.photobucket.com/albums/af281/raperaco/appContainer_zpsmjblx39n.png)

