from onderhoud.models import Complex, Scenario, Scenariogroep, Complexgroep, Deel, Maatregel
from rest_framework import serializers


class MaatregelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maatregel
        fields = ('hoeveelheid', 'eh', 'naam', 'ehprijs_excl', 'prijs_excl', 'btw_percentage', 'start', 'cyclus', 'eind')


class ComplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complex


class ComplexgroepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexgroep


class DeelSerializer(serializers.ModelSerializer):
    maatregelen = MaatregelSerializer(many=True, read_only=True)

    class Meta:
        model = Deel
        fields = ('naam', 'hvh', 'eenheid', 'start', 'eind', 'maatregelen')


class ScenariogroepSerializer(serializers.ModelSerializer):
    delen = DeelSerializer(many=True,read_only=True)

    class Meta:
        model = Scenariogroep
        fields = ('naam', 'delen', )


class ScenarioSerializer(serializers.ModelSerializer):
    scenariogroepen = ScenariogroepSerializer(many=True, read_only=True)

    class Meta:
        model = Scenario
        fields = ('naam', 'start', 'scenariogroepen')
