"""
	Fichero correspondiente a las funciones de las vistas del proyecto.
"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from teams.models import Team
from teams.models import Jugador

from django.http import JsonResponse

from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import TeamSerializer

import random

def formar_equipos(request): 
	"""Forma aleatoriamente los equipos de un team para la partida actual."""
	#componentes = []
	componentes = ['Jinx', 'Lux', 'Karma', 'Ms.Forturne', 'Sejuani', 'Braum', 'Lucian', 'Darius', 'Draven', 'Ezreal']
      
	random.shuffle(componentes)	#mezcla los elementos de la lista,cambiando el orden
    
	jugadores = len(componentes)

	assert jugadores != 0
	print("Test superado con exito")
	
	equipo1 = componentes[0:int(jugadores/2)]

	equipo2 = componentes[int(jugadores/2):]
	
	return render(request, 'formar_equipos.html',{'equipo1':equipo1,'equipo2':equipo2})

class JSONResponse(HttpResponse):
    """
    Una respuesta HTTP que renderiza el contenido en JSON
    """
    def __init__(self,data,**kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def lista_team(request):
    """
    Lista el codigo de todas los equipos, o crea una nueva
    """
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def team_detail(request, pk):
    """
    Recupera,actualiza o borra el codigo de un equipo
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TeamSerializer(team, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        team.delete()
        return HttpResponse(status=204)


	




