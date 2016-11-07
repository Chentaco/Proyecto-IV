
from rest_framework import serializers
from teams.models import Team


class TeamSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=30)
    ciudad = serializers.CharField(max_length=30)

    def create(self, validated_data):
    	"""
    	Crea y valida un nueva instancia de Team
    	"""
    	return Team.objects.create(**validated_data)

    def update(self, instance, validated_data):
    	"""
    	Actualiza y devuelve una instancia existente de Team
    	"""
    	instance.nombre = validated_data.get('nombre', instance.nombre)
    	instance.ciudad = validated_data.get('ciudad', instance.ciudad)

    	instance.save()
    	return instance
