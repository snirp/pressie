from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from onderhoud.models import Scenario, Conditiemeting
from pressie import settings


def home_page(request):
    return render_to_response('home_page.html')


def begroting(request, pk):
    scenario = Scenario.objects.get(pk=pk)
    #json_scenario = JSONRenderer().render(serializer.data)
    return render_to_response('onderhoud/begroting.html', {'scenario': scenario})


def conditiemeting(request, pk):
    cm = Conditiemeting.objects.get(pk=pk)
    #json_scenario = JSONRenderer().render(serializer.data)
    return render_to_response('onderhoud/conditiemeting.html', {'cm': cm})