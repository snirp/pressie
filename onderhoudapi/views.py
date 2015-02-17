from onderhoud.models import Complex, Scenario, Scenariogroep, Complexgroep, Conditiemeting, Conditiegroep, Conditiedeel, \
    Gebrek
from onderhoudapi.serializers import ComplexSerializer, ScenarioSerializer, ScenariogroepSerializer, ComplexgroepSerializer, \
    ConditiemetingSerializer, ConditiegroepSerializer, ConditiedeelSerializer, GebrekSerializer
from pressie import settings
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class ComplexListAPI(generics.ListAPIView):
    queryset = Complex.objects.all()
    serializer_class = ComplexSerializer


class ComplexDetailAPI(generics.RetrieveAPIView):
    queryset = Complex.objects.all()
    serializer_class = ComplexSerializer


class ComplexgroepListAPI(generics.ListAPIView):
    queryset = Complexgroep.objects.all()
    serializer_class = ComplexgroepSerializer


class ComplexgroepDetailAPI(generics.RetrieveAPIView):
    queryset = Complexgroep.objects.all()
    serializer_class = ComplexgroepSerializer


class ScenarioListAPI(generics.ListAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class ScenarioDetailAPI(generics.RetrieveAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class ScenariogroepListAPI(generics.ListAPIView):
    queryset = Scenariogroep.objects.all()
    serializer_class = ScenariogroepSerializer


class ScenariogroepDetailAPI(generics.RetrieveAPIView):
    queryset = Scenariogroep.objects.all()
    serializer_class = ScenariogroepSerializer


class GebrekListAPI(generics.ListAPIView):
    queryset = Gebrek.objects.all()
    serializer_class = GebrekSerializer


class GebrekDetailAPI(generics.RetrieveAPIView):
    queryset = Gebrek.objects.all()
    serializer_class = GebrekSerializer


class ConditiedeelListAPI(generics.ListAPIView):
    queryset = Conditiedeel.objects.all()
    serializer_class = ConditiedeelSerializer


class ConditiedeelDetailAPI(generics.RetrieveAPIView):
    queryset = Conditiedeel.objects.all()
    serializer_class = ConditiedeelSerializer


class ConditiegroepListAPI(generics.ListAPIView):
    queryset = Conditiegroep.objects.all()
    serializer_class = ConditiegroepSerializer


class ConditiegroepDetailAPI(generics.RetrieveAPIView):
    queryset = Conditiegroep.objects.all()
    serializer_class = ConditiegroepSerializer


class ConditiemetingListAPI(generics.ListAPIView):
    queryset = Conditiemeting.objects.all()
    serializer_class = ConditiemetingSerializer


class ConditiemetingDetailAPI(generics.RetrieveAPIView):
    queryset = Conditiemeting.objects.all()
    serializer_class = ConditiemetingSerializer