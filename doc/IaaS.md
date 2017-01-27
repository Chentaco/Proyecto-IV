#Despliegue en un IaaS
##Microsoft Azure
El presente documento está dividido en dos partes: una primera que contendrá las instrucciones **necesarias** para **configurar la cuenta de Azure** y una segunda parte en la que se detalla el resto de pasos (lo que realiza el script) a título informativo.

###Configuración de la cuenta de Azure. Pasos previos a la ejecución del script. (Hacer por el usuario manualmente)
* Instalar el cliente de línea de órdenes (CLI) de Azure:
~~~
sudo apt-get install npm
sudo npm install -g azure-cli
~~~

* Nos logueamos en Azure desde el CLI:
~~~
azure login
~~~

* Obetener las credenciales de tu cuenta Azure:
~~~
azure account download
~~~
Tras ejecutar la orden, nos proporciona un enlace sobre el que pinchar y descargar dichas credenciales en el directorio actual.

* Importamos este fichero de credenciales a nuestro CLI de Azure:
~~~
azure account import ./*.publishsettings
~~~
![azureAccountImport](http://i1016.photobucket.com/albums/af281/raperaco/azureAccountImport_zpsnau5ww1e.png)

* Este fichero ya importado tiene información confidencial, por lo que lo borramos
~~~
rm ./*.publishsettings
~~~

* Generamos los certificados que nos permitirán interaccionar con Azure:
~~~
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout azurevagrant.key -out azurevagrant.key
chmod 600 azurevagrant.key
openssl x509 -inform pem -in azurevagrant.key -outform der -out azurevagrant.cer
~~~

* Subir el certificado (fichero .cer) a Azure. Para ello hacerlo desde https://manage.windowsazure.com en el menú Configuración, en la pestaña Certificados de administración:
![azureCer](http://i1016.photobucket.com/albums/af281/raperaco/azureCer_zpsxqfr6spb.png)

* Crear el fichero .pem que es el que acepta Azure. Dicho fichero .pem contiene tanto la clave privada como la pública:
~~~
openssl req -x509 -key ~/.ssh/id_rsa -nodes -days 365 -newkey rsa:2048 -out azurevagrant.pem
cat azurevagrant.key > azurevagrant.pem
~~~

* En el fichero Vagrantfile de la carpeta deployAzure, modificar los siguientes campos por los propios del usuario:
	* **azure.mgmt_certificate**: (Línea 64) cambiar por la ruta dónde se encuentre el certificado .pem
	* **azure.subscription_id**: (Línea 66) cambiar por el ID de suscripción de la cuenta de Azure del usuario
	* **azure.vm_password**: (Línea 70) cambiar por el password deseado del administrador de la máquina virtual a crear

* En el script deployAzure.sh de la carpeta scripts, cambiar en la última línea la password (Alex2016! en el script de ejemplo) de la máquina virtual por la misma que *azure.vm_password* del apartado anterior .

Con estos pasos realizados correctamente, ya tendremos la cuenta Azure correctamente configurada para aceptar el despliegue realizado desde el script mediante el Vagrantfile y el playbook de Ansible.

* Clonar el repositorio y lanzar el script con:
~~~
git clone git@github.com:mabarrbai/TusPachangas.git
cd TusPachangas/scripts
./deployAzure.sh
~~~

###Resto del proceso de despliegue (lo realiza el script)
* Instalar herramientas generales necesarias
~~~
sudo apt-get update
sudo apt-get install nodejs-legacy
sudo apt-get install npm
sudo apt-get install python-setuptools
sudo easy_install pip
~~~

* Instalar Ansible
~~~
sudo pip install paramiko PyYAML jinja2 httplib2 ansible
~~~

* Descargar e instalar Vagrant
~~~
sudo wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_x86_64.deb
sudo dpkg -i vagrant_1.8.1_x86_64.deb
~~~

* Instalar el plugin de Azure para Vagrant
~~~
vagrant plugin install vagrant-azure
~~~

* Definir la variable de entorno para Ansible en la que indicaremos dónde se encuentra el fichero ansible_hosts:
~~~
export ANSIBLE_HOSTS=~/ansible_hosts
~~~

* Añadimos al fichero ansible_hosts, la nueva máquina que vamos a usar, que será localhost:
~~~
[localhost]
127.0.0.1              ansible_connection=local
~~~

* Crear el playbook a usar de Ansible(playbookTusPachangas.yml):
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
    git: repo=https://github.com/mabarrbai/TusPachangas.git dest=~/appDAI force=yes
    tags:
    - fuentes
    
  - name: Instalar requirements
    pip: requirements=~/appDAI/requirements.txt
    tags:
    - requirements
~~~

* Crear el fabfile.py (Fabric) que se encargará de lanzar la aplicación:
~~~
from fabric.api import run

def ejecutar_app():
	run('sudo nohup python /root/appDAI/manage.py runserver 0.0.0.0:80')
	
def test():
	run('sudo python /root/appDAI/manage.py test')
~~~

Se puede  ver como acaba la ejecución del script con el lanzamiento de la app:
![fabric](http://i1016.photobucket.com/albums/af281/raperaco/fabric_zpsa5xemjqa.png)

* Crear el Vagrantfile:
~~~
Vagrant.configure(2) do |config|
  config.vm.box = "azure"
  config.vm.box_url = 'https://github.com/msopentech/vagrant-azure/raw/master/dummy.box'
  
  config.vm.network "public_network"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.define "localhost" do |l|
          l.vm.hostname = "localhost"
  end
  
  config.vm.provider :azure do |azure, override|
  	azure.mgmt_certificate = '/home/alex/Escritorio/trabajandoIV/pruebaVagrant/azurevagrant.pem'
  	azure.mgmt_endpoint = 'https://management.core.windows.net'
  	azure.subscription_id = '3a08b9a8-264a-49cc-b566-9bf11055fbae'
  	azure.vm_image = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150506-en-us-30GB'
  	azure.vm_name = 'tuspachangas'
  	azure.cloud_service_name = 'tuspachangas'
  	azure.vm_password = 'Alex2016!'
  	azure.vm_location = 'Central US' 
    azure.ssh_port = '22'
    azure.tcp_endpoints = '80:80'
  end
  
  config.vm.provision "ansible" do |ansible|
        ansible.sudo = true
        ansible.playbook = "~/playbookTusPachangas.yml"
        ansible.verbose = "v"
  end
end
~~~

Este fichero Vagrantfile se divide en tres partes.
La primera indica aspectos del box de Vagrant y generales de la máquina virtual que se creará como por ejemplo aspectos de red, y la asignación del nombre localhost.

Una segunda parte en la que se indican características referentes al 'provider' Azure. Las opciones aquí establecidas son algunas de las que pone a disposición el plugin de Azure para Vagrant, todo referente a aspectos de gestión de la máquina virtual como nombre de la máquina, certificados, nombre del servicio en la nube el cual podríamos decir que es equivalente al nombre del dominio (en mi caso será  tuspachangas.cloudapp.net), el usuario administrador de la máquina que si no se indica, por defecto es vagrant, la password de dicho administrador, etc.

Y la tercera parte que se corresponde con la provisión, es decir al uso de ansible por medio del playbook que se le indique.