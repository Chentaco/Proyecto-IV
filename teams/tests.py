from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from teams.models import Team,Jugador

class TeamTestCase(TestCase):
	def setUp(self):
		Team.objects.create(nombre="Los Weyes que invocan", ciudad="Madrid")
		Team.objects.create(nombre="Origen", ciudad="Francia")

	def test_teams_ciudad(self):
		"""Las ciudades de los teams son correctas"""
		
		tWeyes = Team.objects.get(nombre="Los Weyes que invocan")
		tOrigen = Team.objects.get(nombre="Origen")
		
		self.assertEqual(tWeyes.ciudad, 'Madrid')
		self.assertEqual(tOrigen.ciudad, 'Francia')

		print("\nTest: Crear equipo de ranked y ver si es de esa ciudad. Estatus: Superado")

class JugadorTestCase(TestCase):
	def setUp(self):
		tWeyes = Team(nombre="Los Weyes que invocan", ciudad="Madrid")
		tWeyes.save()
		tOrigen = Team(nombre="Origen", ciudad="Francia")
		tOrigen.save()
		
		Jugador.objects.create(nombre="Yin", nickname="Faker", team=tWeyes)
		Jugador.objects.create(nombre="Elchiano", nickname="xPeke", team=tOrigen)

	def test_jugador_pertenece_team(self):
		"""Un jugador pertenece a un equipo"""
		Faker = Jugador.objects.get(nombre="Yin", nickname="Faker")
		Xpeke = Jugador.objects.get(nombre="Elchiano", nickname="xPeke")
		
		tWeyes = Team.objects.get(nombre="Los Weyes que invocan")		
		tOrigen = Team.objects.get(nombre="Origen")
		
		self.assertEqual(Faker.team, tWeyes)
		self.assertEqual(Xpeke.team, tOrigen)

		print("\nTest: Crear jugador e incluirlo en su equipo. Estatus: Superado")

class RutasTeamJSON(APITestCase):
	def test_listar_teams(self):
		"""Listar todas los equipos en JSON"""
		Team.objects.create(nombre="El Tercer Tiempo", ciudad="Granada")
		Team.objects.create(nombre="La Maceta", ciudad="Peligros")

		response = self.client.get('/teams/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response['Content-Type'], 'application/json')

		print("JSON: Ruta '/json/teams/' consultada correctamente")

	def test_detalle_team(self):
		"""Testea el listado de cada equipo individualmente en JSON"""
		Team.objects.create(nombre="El Tercer Tiempo", ciudad="Granada")
		Team.objects.create(nombre="La Maceta", ciudad="Peligros")
		
		teams = Team.objects.values_list('id',flat=True)
		for i in teams:
			response = self.client.get('/teams/'+str(i)+'/')
			self.assertEqual(response.status_code, status.HTTP_200_OK)
			self.assertEqual(response['Content-Type'], 'application/json')
			print("Ruta /teams/" + str(i) + "/ consultada correctamente")
		
		print("JSON: Rutas de cada equipo consultado correctamente.")
