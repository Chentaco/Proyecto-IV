from django.conf.urls import include, url
from teams.views import formar_equipos

urlpatterns = [
    url(r'^match/teams/$', formar_equipos),
]
