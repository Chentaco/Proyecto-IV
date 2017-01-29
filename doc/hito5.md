#Hito Final: Despliegue en un IaaS

Este documento recoge información detallada sobre como realicé el despligue final de mi aplicación en un IaaS. He seguido al dedillo este guión, que me ha ayudado muchísimo: https://unindented.org/articles/provision-azure-boxes-with-vagrant/

##Introduccion

De entre los disponibles, me propuse subirlo a Microsoft Azure. Contraré un mes gratuito, y empecé a hacer pruebas (subidas de contenedores, despliegues de pequeñas aplicaciones, creación y asignación de permisos, etc).  

Finalmente empecé a realizar las configuraciones necesarias para realizar la subida de mi aplicación, las cuales paso a detallas en el siguiente apartado.


##Primeros pasos.

Antes de nada hay que disponer de lo siguiente:  

- Cuenta de Azure:  
Como dije, en mi caso me registré y me subscribí gratuitamente durante un mes a los servicios de azure.  

- Cliente CLI de Azure. 
El cliente CLI lo usaremos para poder usar comandos para realizar las acciones de despligue, configuraciones y demás. Necesito dos paquetes: el npm, que permitirá la instalación del azure-cli, y este último:   

~~~
sudo apt-get install npm
sudo npm install -g azure-cli
~~~

- Estar logueados:  
Para ello ejecutamos el comando:  

~~~
azure login
~~~

Dicha ejecución nos dará un enlace de una dirección web, que tenemos que abrir en nuestro navegador, y una clave. Esta clave la introduciremos en la página web que se nos abre. Tras introducirla, nos dirá que usuario queremos usar como login. Utilizamos aquel **que tiene una subscripcion azure asociada o es coadmin**.  

- Pasar a modo "asm":  

Muchas de las acciones que hay que realizar a continuación no podemos realizarlas con el modo por defecto, utilizamos el comando ```azure config mode asm``` pasa pasar a ese modo.  

- Obetener las credenciales de tu cuenta Azure:  
Necitamos los credeciales de nuestra cuenta, accedemos a ellos con:  
~~~
azure account download
~~~  
Nos dará un enlace donde, al acceder a ese sitio, descargará un archivo con dichos credenciales. Ahora hay que importarlos, por ello nos vamos al directorio donde tenemos ese archivo descargado y ejecutamos:  

~~~
azure account import ./*.publishsettings
~~~  

![img](import)

**NOTA**: Tras el import, es importante borrar o al menos que nacie acceda a dichos archivos. Contiene información confidencial.  

- Crear los certificados para trabajar con Azure:  
Como decía el guión, ahora tocaría crear los certificados, usamos la siguiente orden:  

~~~
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout azurevagrant.key -out azurevagrant.key
chmod 600 azurevagrant.key
openssl x509 -inform pem -in azurevagrant.key -outform der -out azurevagrant.cer
~~~

- Subir el certificado (fichero .cer) a Azure:  
Accedemos a https://manage.windowsazure.com (el portal antiguo) y en el menú Configuración, en la pestaña Certificados de administración, está la opción para subir nuestro certificado:  

![img](subiendo nuestro fichero)  

- Crear el fichero .pem, el cual contiene la clave privada como la pública:

~~~
openssl req -x509 -key ~/.ssh/id_rsa -nodes -days 365 -newkey rsa:2048 -out azurevagrant.pem
cat azurevagrant.key > azurevagrant.pem
~~~

- Configuración del archivo Vagrantfile:  
Yo adjunto en mi repositorio un archivo configurado con datos de información propia. Sin embargo, si alguien quiere usarlo, ha de moficiar los siguiente campos:  
	* **azure.mgmt_certificate**: Que cada uno ponga la ruta de su archivo .pem
	* **azure.subscription_id**: Aquí va la ID de la cuenta azure. Se puede consultar desde el apartado donde subimos el .cer
	* **azure.vm_password**: Poner el password que querais.

- Modificar el script (despliegueazure.sh):  
Para hacerlo todo "medio automático", he creado un script. Dicho script contiene un pasword que usé para el Vagrantfile. Hay que cambiarlo por el que hayais puesto vosotros.  

- Clonar mi respositorio y lanzar el script:  

Ahora solo queda clonar mi repositorio, el que tiene la aplicación, y lanzar dicho script (que está en el respositorio también):  

~~~
git clone git@github.com:Chentaco/Proyecto-IV.git
./despliegueazure.sh
~~~

**NOTA 2**: Si no tiene permisos, darle los necesarios al script.
**NOTA 3**: En caso de que falle el script, probar a ejecutar una a una las ordenes de dicho script (aunque yo lo he comprobado varias veces y funciona).

Si has llegado hasta aquí con todo bien, enhorabuena. Estás preparado para realizar el despliegue.  


##Despliegue

Como dije, el script se encargará de realizar el despliegue automático. Voy a explicar que hace cada una de las órdenes indicadas en dicho documento:  

- Instalación de herramientas básicas
La siguiente parte instala las herramientas minimas que necesitamos para realizar nuestro despliegue:  

~~~
sudo apt-get update
sudo apt-get install nodejs-legacy
sudo apt-get install npm
sudo apt-get install python-setuptools
sudo easy_install pip
~~~

- Instalación de Ansible  
Como indicaba la guia, se necesitaba de Ansible para poder trabajar con nuestro playbook. Dicha instalación se hace con el siguiente comando:  

~~~
sudo pip install paramiko PyYAML jinja2 httplib2 ansible six
~~~

- Descargar e instalar Vagrant y el plugin vagrant-azure:  
Para trabajar con las máquinas de Vagrant. **OJO**: Yo trabajé con vagrant 1.9 PERO al parecer el plugin de azure para vagrant no funciona en esta versión, asi que volví a la 1.8.

~~~
sudo wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_x86_64.deb
sudo dpkg -i vagrant_1.8.1_x86_64.deb
vagrant plugin install vagrant-azure
~~~

- Definir la variable de entorno para Ansible en la que indicaremos dónde se encuentra el fichero ansible_hosts:  
Recordemos de la práctica 5 y 6 que necesito indicarle que hosts son necesarios. Yo ya doy el archivo con mis ansible_hosts usados (el de azure y localhost), solo quedaria importarlo con:  

~~~
export ANSIBLE_HOSTS=~/ansible_hosts
~~~

**NOTA 4**: En caso de que se haya borrado o no se tenga, también añado este comando para que lo añada:  
~~~
[localhost]
127.0.0.1              ansible_connection=local
~~~

- Uso de nuestro playboook, playbookMOBAgestor.yml:  
~~~
- hosts: localhost
  remote_user: vagrant
  become: yes
  become_method: sudo
  tasks:
  - name: Actualizar repositorios
    apt: update_cache=yes
    tags: 
    - apt-update
        
  - name: Instalar dependencias
    apt: name={{ item }}
    with_items:
      - python-setuptools
      - python-dev
      - build-essential
      - python-psycopg2
      - git
    tags:
    - dependencias
    
  - name: easy_install
    easy_install: name=pip
    tags:
    - pip
    
  - name: Descargar fuentes
    git: repo=https://github.com/Chentaco/Proyecto-IV.git dest=~/appDAI force=yes
    tags:
    - fuentes
    
  - name: Instalar requirements
    pip: requirements=~/appDAI/requirements.txt
    tags:
    - requirements  

  - name: Lanzar app
    command: nohup python ~/appDAI/manage.py runserver 0.0.0.0:80
    tags:
    - app
~~~

- **BONUS**: En caso de que la ejecución falle, he eñadiro un fabfile.py, para que lance la aplicación:

~~~
from fabric.api import run

def ejecutar_app():
	run('sudo nohup python /root/appDAI/manage.py runserver 0.0.0.0:80')
	
def test():
	run('sudo python /root/appDAI/manage.py test')
~~~

Si todo ha ido correctamente, la aplicación ya debe estar desplegada en nuestro servidor.  

En caso de que quieras visitarla:  

http://mobagestor.cloudapp.net/

## Anotaciones finales

### Comentarios

Esta versión de la aplicación subida es la usada en la asignatura de DAI SIN los restaurantes y en DJANGO.  

Inicialmente la aplicación empezó a ser desarrollada en Flask, pero más tarde tuve que cambiar su diseño y servicios por lo que hay ahora. Además no tiene la opción que se pedía en prácticas de DAI que era la de añadir restaurantes y demás. En su lugar está lo de añadir equipos y jugadores.

### Sobre el Vagrantfile:

Tras muchas configuraciones, la estructura de mi Vagrantfile es la siguiente:  


 Crear el Vagrantfile:
~~~
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "azure"
  config.vm.box_url = 'https://github.com/msopentech/vagrant-azure/raw/master/dummy.box'
  
  config.vm.network "public_network"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.define "localhost" do |l|
          l.vm.hostname = "localhost"
  end
   
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.
  config.vm.provider :azure do |azure, override|
  	azure.mgmt_certificate = '/home/chentaco/Documentos/IV/ladeazure/azurevagrant.pem'
  	azure.mgmt_endpoint = 'https://management.core.windows.net'
  	azure.subscription_id = '562af239-6337-4c9c-bf71-47483eff05eb'
  	azure.vm_image = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150506-en-us-30GB'
  	azure.vm_name = 'mobagestor'
  	azure.cloud_service_name = 'mobagestor'
  	azure.vm_password = 'Chente@dmin'
  	azure.vm_location = 'West Europe' 
        azure.ssh_port = '22'
        azure.tcp_endpoints = '80:80'
  end
  
  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL
  config.vm.provision "ansible" do |ansible|
        ansible.sudo = true
        ansible.playbook = "playbookMOBAgestor.yml"
        ansible.verbose = "v"
  end
end
~~~

Podemos observar como dicho archivo tiene los parámetros configurados personales, como son nuestras personal key, passwor,d usuarios, etc. como inficamos al principio. Cada uno tiene que editar los suyos. También vemos que tiene opciones referentes a Azure, como que dispone del plugin, la gestión de la máquina virtual, etc. Finalmente tenemos que ejecute el playbook que creamos.

## Para terminar

Decir que actualmente la web está en un periodo gratuito de un mes. Supongo que para fechas después del 27/01/2017 estará caida. 