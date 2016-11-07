from django.conf.urls import include, url
from teams import views

urlpatterns = [
    url(r'^match/teams/$', views.formar_equipos),
    url(r'^teams/$', views.lista_team),
    url(r'^teams/(?P<pk>[0-9]+)/$', views.team_detail),
]
