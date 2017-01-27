from django.conf.urls import patterns, url
from teams import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
        url(r'^reclama_datos/$', views.reclama_datos, name='reclama_datos'),
        url(r'^megusta_jugador/$', views.megusta_jugador, name='megusta_jugador'),
        url(r'^json/teams/$', views.lista_team),
    	url(r'^json/teams/(?P<pk>[0-9]+)/$', views.team_detail),
        url(r'^(?P<team_name>[\w\-]+)/$', views.team, name='team'),
        url(r'^(?P<team_name>[\w\-]+)/add_jugador/$', views.add_jugador, name='add_jugador'),               
        )
