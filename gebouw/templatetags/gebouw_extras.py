from django import template


register = template.Library()

@register.inclusion_tag('gebouw/inclusion/conditie-overzicht.html')
def show_conditie_overzicht(conditiemeting):
    return {'conditiemeting': conditiemeting}

@register.inclusion_tag('gebouw/inclusion/conditie-uitgelicht.html')
def show_conditie_uitgelicht(conditiemeting):
    return {'conditiemeting': conditiemeting}

@register.inclusion_tag('gebouw/inclusion/begroting-overzicht.html')
def show_begroting_overzicht(conditiemeting):
    return {'scenario': conditiemeting.scenario}

@register.inclusion_tag('gebouw/inclusion/begroting-onderbouwing.html')
def show_begroting_onderbouwing(conditiemeting):
    return {'scenario': conditiemeting.scenario}