from fabric.api import run

def ejecutar_app():
	run('sudo nohup python /root/appDAI/manage.py runserver 0.0.0.0:80')
	
def test():
	run('sudo python /root/appDAI/manage.py test')	
