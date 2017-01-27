#Despliegue de la aplicación en un PaaS

Los pasos llevados a cabo para desplegar mi aplicación en Heroku han sido los siguientes:
* Registrarme en Heroku, obviamente.
* Descargar el toolbelt de Heroku, el cual nos proporciona una serie de herramientas necesarias para poder trabajar con Heroku.
~~~
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
~~~
* Nos logueamos en Heroku desde el terminal.
~~~ 
heroku login
~~~
* Crear un fichero **Procfile** en la carpeta raíz de nuestro proyecto, en el que indicamos los pasos necesarios para desplegar la aplicación web en Heroku. En nuestro caso:
~~~
web: gunicorn TusPachangas.wsgi --log-file -
~~~
* Actualizar el fichero de dependencias **requirements.txt**. Tras actualizarlo, borrar la entrada correspondiente a nuestra aplicación ya que no es una dependencia, sino el objetivo a conseguir. En mi caso, TusPachangas.
~~~
pip freeze > requirements.txt
~~~
* Modificar el fichero **settings.py** para indicar que cuando la aplicación se encuentre en Heroku, use la base de datos que provee Heroku. Para ello, hay que obtener la URL de la base de datos de Heroku la cual se puede obtener desde el panel de control de Heroku. El código a añadir al fichero será el siguiente:
~~~
import dj_database_url
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
ON_HEROKU = os.environ.get('PORT')
if ON_HEROKU:
    DATABASE_URL='postgres://fhtyiztxysbrdn:WI7TLSaRrLYxotdwfryDYIQwn2@ec2-54-225-192-128.compute-1.amazonaws.com:5432/demv8ll9orcqeg'
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}
~~~
* En el fichero wsgi.py, añadir el siguiente código:
~~~
from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())
~~~
* Preparar todos los ficheros modificados para subirlos a un repositorio GitHub.
~~~
git init
git add .
git commit -m "my django app"
~~~
* Crear un nuevo repositorio remoto git para subir la aplicación a Heroku.
~~~
heroku create
~~~
* Subir la aplicación al nuevo repositorio creado.
~~~
git push heroku master
~~~
* Aplicar los cambios sobre la base de datos de Heroku y crear el superusuario de nuestra aplicación.
~~~
heroku run python manage.py makemigrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
~~~
* Ya se puede abrir la aplicación desplegada.
~~~
heroku open
~~~
* Vemos que el comando anterior nos abre una ventana de navegador con nuestra aplicación desplegada (si es que todo ha salido bien) pero con una URL un tanto rara. Si se quiere cambiar, se puede hacer desde el panel de control de Heroku, en la pestaña Ajustes. Una vez cambiado, hay que actualizar el nombre del repositorio remoto de nuestra aplicación con el nuevo nombre, para ello hay que ejecutar(en mi caso):
~~~
git remote rm heroku
heroku git:remote -a tuspachangas
~~~

Habiendo realizado estos pasos citados sin errores, la aplicación ya estará desplegada en Heroku, usando la base de datos PostgreSQL que Heroku proporciona.Ya solo queda rellenar la base de datos, lo cual puede realizarlo el superusuario de la aplicación  creado anteriormente en la ruta **/admin/**.
Por tanto, mi aplicación desplegada en el servicio gratuito de Heroku tendrá la URL **https://tuspachangas.herokuapp.com/** y queda de la siguiente forma:
* La ruta **/**
![heroku](http://i1016.photobucket.com/albums/af281/raperaco/heroku_zpsgojniwgh.png)
* La ruta **/penhas/**
![heroku1](http://i1016.photobucket.com/albums/af281/raperaco/heroku1_zpswwx1rjgb.png)
* Las rutas en las que se muestra en detalle cada peña individualmente. Se accede a traves del identificador pk, el cual se puede ver que se obtiene en la ruta /penhas/ en la anterior imagen. Por ejemplo para la peña con identificador 2, la ruta será **/penhas/2/**
![heroku2](http://i1016.photobucket.com/albums/af281/raperaco/heroku2_zpsyw5ew7gr.png)

Además de todo lo anterior, que sería lo básico para desplegar la aplicación en Heroku, he conectado GitHub con Heroku para realizar un despliegue automático cada vez que se suban nuevos fuentes al repositorio GitHub de la aplicación habiendo superado previamente los tests. De esta forma, cada vez que modifique un fichero fuente y lo suba al repositorio con la orden **git push**, automáticamente la aplicación será testeada con los nuevos cambios en Travis y SnapCI y si los tests se superan, la aplicación será desplegada con los nuevos cambios en Heroku.

Hay un enlace a mi aplicación desplegada en Heroku a través de la URL antes citada, o a través del badge que hay al inicio de este documento.