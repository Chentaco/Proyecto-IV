[![Build Status](https://travis-ci.org/Chentaco/Proyecto-IV.svg?branch=master)](https://travis-ci.org/Chentaco/Proyecto-IV)  
  
[![Build Status](https://snap-ci.com/Chentaco/Proyecto-IV/branch/master/build_image)](https://snap-ci.com/Chentaco/Proyecto-IV/branch/master)  
  
[![Heroku Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Chentaco/Proyecto-IV/tree/master) 


# Proyecto-IV
Repositorio de la asignatura Infraestructura Virtual de la ETSIIT de Granada. El proyecto de la asignatura será realizado junto al proyecto de DAI. 
  
-------------------------------- 

##Información:  

**Autor**: Ramón Sánchez García  
**Contacto**: chentaco@correo.ugr.es  
**Aplicacion**: MOBAgestor, gestor de tus equipos y partidas de tipo MOBA  
**Lenguaje**: Python3  
**Framework**: Django   
**PasS**: Heroku 
  
--------------------------------  
##Introducción

La idea que estoy llevando a cabo es la de hacer una aplicación web para esta asignatura. Dicha aplicación se encargará de la gestión de equipos y mini-torneos, muestreo de resultados, etc. de los famosos videojuegos tipo [MOBA](https://es.wikipedia.org/wiki/Multiplayer_online_battle_arena). En dicha Web se podrá registrar tu usuario junto a tu equipo, o encontrar otro equipo, participar en torneos solo o acompañado de tus amigos, ver tus resultados en torneos o partidas importantes, crear tus propios torneos, etc.  



##Desarrollo 

Se utilizarán las siguientes herramientas:   

* Disponer de un **servidor web**, el cual se configurará para albergar la aplicación.
* **Servidor de base de datos** para guardar y almacenar los datos y demás contenido de la aplicación web, como los datos de los usuarios.
* **Servidor de correo/bot de Telegram (aun no está decidido si finalmente se hará)** para avisar a los usuarios de dicha aplicación sobre novedades.
* **Herramientas**: Para programar, el lenguaje utilizado ha sido [Python3](https://www.python.org/download/releases/3.0/), el framework usado ha sido [Django](https://www.djangoproject.com/), y [Travis CI](https://travis-ci.org/) para testear la web.  

  
El uso de más herramientas, cambios y actualizaciones futuras se verán reflejadas en esta parte del documento.

--------------------------------

##Tests E Integración Continua

Uno de los objetivos más importantes que llevaremos sobre nuestro proyecto será usar un sistema de testeos para comprobar que todo está bien. Como he dicho arriba, yo he utilizado Django el cual contiene un método para realizar estos tests usando una de sus subclases llamada [TestCase](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.TestCase). Para ello, en el archivo generado **test.py** he escrito una serie de condiciones que servirán como test para comprobar que todo va correcto. Actualmente tiene muy pocas ordenes, las básicas para lo que hay desarrollado, pero se supone que esto irá cambiando junto al avance del proyecto.  

  
Lo siguiente ha sido utilizar una herramienta de integración continua. En mi caso he utilizado **Travis CI** ya que es la que recomiendan y que podemos registrarnos en ella directamente con nuestra cuenta de **Github**. Necesitamos crear para ello un archivo en nuestro directorio llamado **.travis.yml** en el cual indicamos las herramientas que vamos a usar, python3 en mi caso. Después tras cada push, la página debería realizar las pruebas de integración de forma **automática**. Además, para comprobar si ha pasado las pruebas, Travis CI ofrece una especie de banner que permite informar que nuestro proyecto las ha superado. Podemos observarla al comienzo de este documento.  
  
-------------------------------  
  
##Uso de PaaS  
  
Otro de los objetivos es el uso de algún PaaS (en mi caso [Heroku](https://www.heroku.com)), para desplegar una aplicación y tener parte del trabajo de instalación ya hecho. He utilizado este ya que es con el que más he trabajado en estos últimos días. También utilicé Openshift, pero con este último no me he terminado de familiarizar.  
  
En Heroku he dado de alta mi aplicación, visible desde los siguientes enlaces:  
  
* [http://mobagestor.herokuapp.com/match/teams/](http://mobagestor.herokuapp.com/match/teams/) Para visualizar la aplicación de formación de equipos aleatoria.  
* [http://mobagestor.herokuapp.com/teams/](http://mobagestor.herokuapp.com/teams/) Para visualizar un listado de los equipos.  
* También se puede acceder a un equipo en concreto añadiendo su *primarykey* al final de la ruta, ej. /teams/1/ para el equipo cuya pk es 1.  
* **Actualmente no hay nada en el main, por lo que si se accede a (/), saldrá un error.**  
  
También se ha realizado tests usando [Snap-CI](https://snap-ci.com/), donde se creó un test personalizado, y Heroku se encargará del despliegue automático si el test se ha pasado. El resultado del test:  
  
[![Build Status](https://snap-ci.com/Chentaco/Proyecto-IV/branch/master/build_image)](https://snap-ci.com/Chentaco/Proyecto-IV/branch/master)  
  
Aunque ya utilizamos Travis, el uso de CI es más simple para utilizarlo en Heroku. 
  
También se ha configurado Heroku para que, una vez superado el test, se realize el despliegue automático en Heroku.  
  
Para el despliegue manual en Heroku he creado el siguiente botón:  
  
[![Heroku Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Chentaco/Proyecto-IV/tree/master)  
  
Toda esta configuración relacionado con el **PaaS** está descrita y documentada en la parte de ejercicios del **Tema 3**, donde utilicé el propio proyecto para realizar los ejercicios de dicho tema y describen detalladamente como he realizado cada paso. Puedes consultarlos en el [siguiente enlace](https://github.com/Chentaco/EjerciciosIV/blob/master/tema3.md). 

-------------------------------  

##Contenedores

Otro de los objetivos fue el uso de contenedores, pequeñas "máquinas virtuales" donde ejecutar nuestro proyecto. Dichos contenedores se crean con el SO que nosotros queramos, (en mi caso elegí la última de ubuntu), donde va nuestra aplicación dentro de ella. Existen varios métodos, como por ejemplo Docker, el cual fue el que más enfásis le puse en esta parte de la práctica.  

Además subimos nuestro proyecto al repositorio de contenedores de [Docker](). Dicha web permite lanzar nuestro contenedores online, si disponemos de algún servicio de "nodes", como dice la propia web (Amazon, Azure, ...). Actualmente no dispongo de cuenta en ningún servicio, por lo que no se puede ver online el contenedor.  

Puedes visitar mi respositorio Docker en el siguiente enlace:  

[https://cloud.docker.com/app/chentaco/repository/list/](https://cloud.docker.com/app/chentaco/repository/list/)  

Además adjunto el siguiente [script](), incluido en el repositorio del Proyecto, que permite descargar y arrancar el contenedor de mi proyecto automáticamente. El único problema es que el proyecto ha de arrancarse manualmente, asi que una vez arrancado el contenedor, ejecutamos:  

```python /Proyecto-IV/manage.py runserver 0.0.0.0:5500```  
  
Ahora necesitamos ver que ip tiene asignada nuestro proyecto, para ello, en el contenedor, miramos la ip de este con el comando ```ip address```, utilizando ella en el navegador, junto el puerto **5500** que es el asignado.
  
  
