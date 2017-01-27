from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from teams.models import Team,Jugador

class TeamTestCase(TestCase):
	def setUp(self):
		Team.objects.create(nombre="El Tercer Tiempo", ciudad="Granada", direccion="Recogidas 1, Granada, Spain")
		Team.objects.create(nombre="La Maceta", ciudad="Peligros",direccion="Av. Pechuelos 1, Peligros, Granada, Spain")

	def test_teams_ciudad(self):
		"""Las ciudades de las teams son correctas"""
		pMaceta = Team.objects.get(nombre="La Maceta")
		pTercerTiempo = Team.objects.get(nombre="El Tercer Tiempo")

		self.assertEqual(pMaceta.ciudad, 'Peligros')
		self.assertEqual(pMaceta.direccion, 'Av. Pechuelos 1, Peligros, Granada, Spain')
		self.assertEqual(pTercerTiempo.ciudad, 'Granada')
		self.assertEqual(pTercerTiempo.direccion, 'Recogidas 1, Granada, Spain')
		print("Test de creacion de team correcto y superado.")

class JugadorTestCase(TestCase):
	def setUp(self):
		pTercerTiempo = Team(nombre="El Tercer Tiempo", ciudad="Granada", direccion="Recogidas 1, Granada, Spain")
		pTercerTiempo.save()
		pMaceta = Team(nombre="La Maceta", ciudad="Peligros",direccion="Av. Pechuelos 1, Peligros, Granada, Spain")
		pMaceta.save()
		Jugador.objects.create(nick="Andres", name="Iniesta", team=pMaceta)
		Jugador.objects.create(nick="Cristiano", name="Biraghi", team=pTercerTiempo)

	def test_jugador_pertenece_team(self):
		"""Un jugador pertenece a un team"""
		Iniesta = Jugador.objects.get(nick="Andres", nombre="Iniesta")
		Biraghi = Jugador.objects.get(nick="Cristiano", nombre="Biraghi")
		
		pMaceta = Team.objects.get(nombre="La Maceta")
		pTercerTiempo = Team.objects.get(nombre="El Tercer Tiempo")

		self.assertEqual(Iniesta.team, pMaceta)
		self.assertEqual(Biraghi.team, pTercerTiempo)
		print("Test de creacion de jugador y pertenencia a un team correcto y superado.")

class RutasTeamsJSON(APITestCase):
	def test_listar_teams(self):
		"""Listar todas los teams en JSON"""
		Team.objects.create(nombre="El Tercer Tiempo", ciudad="Granada")
		Team.objects.create(nombre="La Maceta", ciudad="Peligros")

		response = self.client.get('/match/team/json/teams/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response['Content-Type'], 'application/json')

		print("JSON: Ruta '/json/teams/' consultada correctamente")

	def test_detalle_team(self):
		"""Testea el listado de cada team individualmente en JSON"""
		Team.objects.create(nombre="El Tercer Tiempo", ciudad="Granada")
		Team.objects.create(nombre="La Maceta", ciudad="Peligros")
		
		teams = Team.objects.values_list('id',flat=True)
		for i in teams:
			response = self.client.get('/match/team/json/teams/'+str(i)+'/')
			self.assertEqual(response.status_code, status.HTTP_200_OK)
			self.assertEqual(response['Content-Type'], 'application/json')
			print("Ruta /teams/" + str(i) + "/ consultada correctamente")
		
		print("JSON: Rutas de cada team consultada correctamente.")
