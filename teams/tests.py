from django.test import TestCase

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
