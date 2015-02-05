from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from onderhoud.models import Scenario, Conditiemeting, Conditiefoto, Complex
from pressie import settings


def home_page(request):
    return render_to_response('home_page.html')


def begroting(request, pk):
    scenario = Scenario.objects.get(pk=pk)
    return render_to_response('onderhoud/begroting.html', {'scenario': scenario})


def conditiemeting(request, pk):
    cm = Conditiemeting.objects.get(pk=pk)
    return render_to_response('onderhoud/conditiemeting.html', {'cm': cm})


def conditiefoto(request, pk):
    cf = Conditiefoto.objects.get(pk=pk)
    return render_to_response('onderhoud/conditiefoto.html', {'cf': cf})


def complex_list(request):
    cx_list = Complex.objects.all()
    return render_to_response('onderhoud/complex-list.html', {'cx_list': cx_list})