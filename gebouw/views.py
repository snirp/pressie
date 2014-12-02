from django.http import Http404
from django.shortcuts import render_to_response
from django.views import generic
from gebouw.models import Complex, Conditiemeting, Scenario


class ComplexIndex(generic.ListView):
    model = Complex


class ComplexDetail(generic.DetailView):
    model = Complex


class ConditiemetingDetail(generic.DetailView):
    model = Conditiemeting


class ConditiemetingGroepen(ConditiemetingDetail):
    template_name = 'gebouw/conditiemeting_groepen.html'


def scenario_detail(request, s_id):
    try:
        s = Scenario.objects.get(pk=s_id)
    except Scenario.DoesNotExist:
        raise Http404
    jaar_range = range(s.start, s.eind + 1)
    m_list = []
    sgrp_list = []
    for sgrp in s.scenariogroep_set.all():
        sgrp_dict = {}
        sgrp_dict['scenariogroep'] = sgrp
        for d in sgrp.deel_set.all():
            for m in d.maatregel_set.all():
                if m.start <= s.eind:
                    #tijdelijke(?) fix for maatregelen die geheel buiten scenario periode vallen
                    m_dic = {}
                    m_dic['maatregel'] = m
                    m_dic['jaren'] = m.get_jaarbedragen(jaar_range)
                    m_list.append(m_dic)

    return render_to_response('gebouw/scenario_detail.html', {'s': s, 'jaar_range': jaar_range, 'm_list': m_list})


def scenario_report_vve(request, s_id):
    try:
        s = Scenario.objects.get(pk=s_id)
    except Scenario.DoesNotExist:
        raise Http404
    return render_to_response('gebouw/scenario_report_vve.html', {'s': s})