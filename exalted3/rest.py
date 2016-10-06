from rest_framework import serializers, viewsets
from channels_api.bindings import ResourceBinding
from storyteller.exalted3.models import Persona, Stat


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat


class TemplateBinding(ResourceBinding):
    model = Persona
    stream = 'questions'
    serializer_class = PersonaSerializer
    queryset = Persona.objects.all()


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class StatViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer