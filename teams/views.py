from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

#imports
from teams.models import Team
from teams.models import Jugador
from teams.forms import JugadorForm

from django.http import JsonResponse

from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import TeamSerializer

#indice
def index(request):
	team_list = Team.objects.order_by('nombre')[:10]
	jugador_list = Jugador.objects.order_by('-megusta')[:10]
	context_dict = {'teams': team_list, 'jugadores': jugador_list}
	return render(request, 'match_teams/index.html', context_dict)

#
#about
def about(request):
	context_dict = {'boldmessage': "Esta es la pagina /about/"}
	return render(request, 'match_teams/about.html', context_dict)		
    
#equipos
def team(request, team_name):

    context_dict = {}

    try:
        team = Team.objects.get(slug=team_name)
        context_dict['team_name'] = team.nombre

        jugadores = Jugador.objects.filter(team=team)

        context_dict['jugadores'] = jugadores
        
        context_dict['team'] = team

        #actualizar el contador de visitas
        team.visitas = team.visitas + 1
        team.save()

    except Team.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'match_teams/team.html', context_dict)

#jugadores
def add_jugador(request, team_name):
    try:
        team = Team.objects.get(slug=team_name)
    except Team.DoesNotExist:
        team = None

    if request.method == 'POST':        

        if team != None:    
            form = JugadorForm(request.POST)

            if form.is_valid():
                #obtengo los valores del formulario del nuevo jugador pero no los envio para anhadir el team obtenida de la URL
                jugador = form.save(commit=False)

                jugador.team = team

                jugador.save()
                return HttpResponseRedirect('/match/teams/%s/' % team.slug)
            else:
                print (form.errors)
        else:
            print ('El team '+team_name+' no existe. No se puede insertar un jugador en un team inexistente.')
    else:    
        form = JugadorForm()

    return render(request, 'match_teams/add_jugador.html', {'form': form, 'team': team})

def reclama_datos(request):
    lista_teams = Team.objects.order_by('-visitas')[0:5]
     
    datos = {}

    datos['teams'] = [lista_teams[0].nombre,lista_teams[1].nombre,lista_teams[2].nombre,lista_teams[3].nombre,lista_teams[4].nombre]

    datos['visitas'] = [lista_teams[0].visitas,lista_teams[1].visitas,lista_teams[2].visitas,lista_teams[3].visitas,lista_teams[4].visitas]
   
    return JsonResponse(datos,safe=False)

def megusta_jugador(request):
    datos = {}

    jug_id = None
    if request.method == 'GET':
    	jug_id = request.GET['jugador_id']
    	
    megusta = 0
    if jug_id:
    	jug = Jugador.objects.get(id=int(jug_id))
    	if jug:
    		megusta = jug.megusta + 1
    		jug.megusta = megusta
    		jug.save()
	
	return HttpResponse(megusta)
	
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
