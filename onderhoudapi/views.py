
from onderhoud.models import Complex, Scenario, Scenariogroep, Complexgroep
from onderhoudapi.serializers import ComplexSerializer, ScenarioSerializer, ScenariogroepSerializer, ComplexgroepSerializer
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


class ScenarioDetailAPI(generics.RetrieveAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class ScenariogroepListAPI(generics.ListAPIView):
    queryset = Scenariogroep.objects.all()
    serializer_class = ScenariogroepSerializer


class ScenariogroepDetailAPI(generics.RetrieveAPIView):
    queryset = Scenariogroep.objects.all()
    serializer_class = ScenariogroepSerializer
