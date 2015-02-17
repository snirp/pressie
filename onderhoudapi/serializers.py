from onderhoud.models import Complex, Scenario, Scenariogroep, Complexgroep, Deel, Maatregel, Gebrek, Conditiedeel, \
    Conditiegroep, Conditiemeting
from rest_framework import serializers


# # # gebreken # # #

class GebrekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gebrek
        fields = ('naam', 'get_type', 'get_omvang_waarde', 'get_intensiteit_waarde', 'get_ernst_waarde')


class ConditiedeelSerializer(serializers.ModelSerializer):
    gebrek_set = GebrekSerializer(many=True, read_only=True)

    class Meta:
        model = Conditiedeel
        fields = ('__str__', 'conditiescore', 'gebrek_set', )


class ConditiegroepSerializer(serializers.ModelSerializer):
    conditiedeel_set = ConditiedeelSerializer(many=True, read_only=True)

    class Meta:
        model = Conditiegroep
        fields = ('__str__', 'conditie', 'conditiedeel_set')


class ConditiemetingSerializer(serializers.ModelSerializer):
    conditiegroep_set = ConditiegroepSerializer(many=True, read_only=True)

    class Meta:
        model = Conditiemeting
        fields = ('complex_code', 'complex_naam', 'datum', 'conditiegroep_set')


# # # Complexen # # #

class ComplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complex


class ComplexgroepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexgroep


# # # Scenarios # # #

class MaatregelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maatregel
        fields = ('hoeveelheid', 'eh', 'naam', 'ehprijs_excl', 'prijs_excl', 'btw_percentage', 'start', 'cyclus', 'eind')


class DeelSerializer(serializers.ModelSerializer):
    maatregelen = MaatregelSerializer(many=True, read_only=True)

    class Meta:
        model = Deel
        fields = ('naam', 'hvh', 'eenheid', 'start', 'eind', 'maatregelen')


class ScenariogroepSerializer(serializers.ModelSerializer):
    delen = DeelSerializer(many=True, read_only=True)

    class Meta:
        model = Scenariogroep
        fields = ('naam', 'delen', )


class ScenarioSerializer(serializers.ModelSerializer):
    scenariogroepen = ScenariogroepSerializer(many=True, read_only=True)

    class Meta:
        model = Scenario
        fields = ('naam', 'start', 'scenariogroepen')

