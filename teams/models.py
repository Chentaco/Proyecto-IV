from django.db import models

class Team(models.Model):
	nombre = models.CharField(max_length=30)
	ciudad = models.CharField(max_length=30)

	class Meta:
		ordering = ["nombre"]

	def __str__(self):
		return '%s de %s' %(self.nombre, self.ciudad)

class Jugador(models.Model):
	nombre = models.CharField(max_length=40)
	nickname = models.CharField(max_length=50)
	team = models.ForeignKey(Team)

	class Meta:
		ordering = ["team"]
	
	def __str__(self):
		return '%s %s' %(self.nombre, self.nickname)

	
	
