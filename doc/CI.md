#Sistemas de tests e Integración continua
En este fichero .travis.yml he indicado las instrucciones para instalar y testear la aplicación web. Para ello he utilizado las órdenes a través de la herramienta de construcción make con el fichero Makefiile, ya explicado en el paso anterior.
De esta manera, estamos haciendo una comprobación doble. Por una parte se prueba que el fichero Makefile que tenga el formato correcto y realice las operaciones adecuadas, y por otra parte se prueba la instalación y testeo de la aplicación web.
Se puede ver el resultado de las pruebas superadas de integración continua con Travis en las siguientes imágenes:
* Enlace directo al testeo en Travis:[![Build Status](https://travis-ci.org/mabarrbai/TusPachangas.svg?branch=master)](https://travis-ci.org/mabarrbai/TusPachangas)
* Capturas tomadas desde Travis:
![TravisMake1](http://i1016.photobucket.com/albums/af281/raperaco/travisMake1_zpswr5eafgc.png)
![TravisMake2](http://i1016.photobucket.com/albums/af281/raperaco/travisMake1_zps2wkpmeas.png)
![TravisMake3](http://i1016.photobucket.com/albums/af281/raperaco/travisMake2_zpsfmoiny2p.png)
