from django.db import models

from django.template.defaultfilters import slugify

class Team(models.Model):

	nombre = models.CharField(max_length=30)
	ciudad = models.CharField(max_length=30)
	visitas = models.IntegerField(default=0, editable = False)
	direccion = models.CharField(max_length=70)
	slug = models.SlugField(unique=True,default='')

	def save(self, *args, **kwargs):
                self.slug = slugify(self.nombre)
                super(Team, self).save(*args, **kwargs)

	class Meta:
		ordering = ["nombre"]

	def __unicode__(self):
		return '%s de %s' %(self.nombre, self.ciudad)

class Jugador(models.Model):

	nick = models.CharField(max_length=40)
	name = models.CharField(max_length=60)
	team = models.ForeignKey(Team)
	megusta = models.IntegerField(default=0, editable=False)
	slug = models.SlugField(unique=True,default='')

	def save(self, *args, **kwargs):
                self.slug = slugify(self.team.nombre+self.nick+self.name)
                super(Jugador, self).save(*args, **kwargs)

	class Meta:
		ordering = ["team"]
	
	def __unicode__(self):
		return 'Nick: %s. Nombre real: %s' %(self.nick, self.name)
