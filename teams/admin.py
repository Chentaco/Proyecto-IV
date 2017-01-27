from django.contrib import admin

from teams.models import Team, Jugador

class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('nombre',)}

admin.site.register(Team, TeamAdmin)
admin.site.register(Jugador)
