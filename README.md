[![Build Status](https://travis-ci.org/Chentaco/Proyecto-IV.svg?branch=master)](https://travis-ci.org/Chentaco/Proyecto-IV)

# Proyecto-IV
Repositorio de la asignatura Infraestructura Virtual de la ETSIIT de Granada. El proyecto de la asignatura será realizado junto al proyecto de DAI. 
  
-------------------------------- 

##Información:  

**Autor**: Ramón Sánchez García  
**Contacto**: chentaco@correo.ugr.es  
**Aplicacion**: MOBAgestor, gestor de tus equipos y partidas de tipo MOBA  
**Lenguaje**: Python3  
**Framework**: Django  
  
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
  

