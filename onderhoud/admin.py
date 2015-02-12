from django.contrib import admin
from .models import Complex, Complexgroep, Complexdeel, Scenario, Scenariogroep, Deel, Maatregel, \
    Conditiemeting, Conditiegroep, Conditiedeel, Gebrek, Conditiefoto, Hoofdgroep, Hoofdcodering, Codering, \
    Element, Activiteit, Gebrektype, Nengebrek, Deelactiviteit, ActiviteitOnderbouwing, Btw


class NengebrekAdmin(admin.ModelAdmin):
    list_display = ('naam', 'gebrektype', 'generiek', )


class ActiviteitOnderbouwingInline(admin.TabularInline):
    model = ActiviteitOnderbouwing


class ActiviteitAdmin(admin.ModelAdmin):
    list_display = ('naam', 'generiek', )
    inlines = [ActiviteitOnderbouwingInline]


class CoderingInline(admin.TabularInline):
    model = Codering
    extra = 1


class HoofdcoderingAdmin(admin.ModelAdmin):
    inlines = [CoderingInline]
    list_display = ('code', 'naam',)


class CoderingAdmin(admin.ModelAdmin):
    list_display = ('code', 'hoofdcodering', 'naam')
    search_fields = ('code', 'naam', 'hoofdcodering__naam')


class ElementAdmin(admin.ModelAdmin):
    list_display = ('naam', 'eenheid', 'vervangwaarde', 'codering')
    search_fields = ('naam', )
    list_filter = ('eenheid', )


class ComplexgroepInline(admin.TabularInline):
    model = Complexgroep


class ComplexAdmin(admin.ModelAdmin):
    inlines = [ComplexgroepInline]
    list_display = ('code', 'naam',)


class ComplexdeelInline(admin.TabularInline):
    model = Complexdeel


class ComplexgroepAdmin(admin.ModelAdmin):
    inlines = [ComplexdeelInline]
    list_display = ('complex', 'naam',)
    list_filter = ('complex',)


class ScenariogroepInline(admin.TabularInline):
    model = Scenariogroep


class ScenarioAdmin(admin.ModelAdmin):
    inlines = [ScenariogroepInline]
    list_display = ('complex', 'naam', 'start')


class ConditiegroepInline(admin.TabularInline):
    model = Conditiegroep


class ConditiemetingAdmin(admin.ModelAdmin):
    inlines = [ConditiegroepInline]
    list_display = ('complex_naam', 'datum', 'scenario')


class ComplexdeelAdmin(admin.ModelAdmin):
    list_display = ('element', 'complexgroep', 'complex_naam')


class MaatregelInline(admin.TabularInline):
    model = Maatregel


class DeelAdmin(admin.ModelAdmin):
    list_display = ('get_scenario', 'scenariogroep', 'naam', 'hvh')
    inlines = [MaatregelInline]


class GebrekInline(admin.TabularInline):
    model = Gebrek


class ConditiefotoInline(admin.TabularInline):
    model = Conditiefoto


class ConditiedeelAdmin(admin.ModelAdmin):
    inlines = [GebrekInline, ConditiefotoInline]
    list_display = ('conditiegroep', 'deel', 'conditiescore', 'get_complex_str', 'get_conditiemeting_str' )
    list_filter = ('conditiescore', 'conditiegroep')


class MaatregelAdmin(admin.ModelAdmin):
    list_display = ('naam', 'hvh', 'eh')


class DeelInline(admin.TabularInline):
    model = Deel


class ScenariogroepAdmin(admin.ModelAdmin):
    inlines = [DeelInline]


admin.site.register(Btw)
admin.site.register(Deelactiviteit)
admin.site.register(Hoofdgroep)
admin.site.register(Hoofdcodering, HoofdcoderingAdmin)
admin.site.register(Codering, CoderingAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(Activiteit, ActiviteitAdmin)
admin.site.register(Gebrektype)
admin.site.register(Nengebrek, NengebrekAdmin)
admin.site.register(Complex, ComplexAdmin)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Conditiemeting, ConditiemetingAdmin)
admin.site.register(Complexdeel, ComplexdeelAdmin)
admin.site.register(Deel, DeelAdmin)
admin.site.register(Conditiedeel, ConditiedeelAdmin)
admin.site.register(Maatregel, MaatregelAdmin)
admin.site.register(Scenariogroep, ScenariogroepAdmin)
admin.site.register(Conditiegroep)
admin.site.register(Complexgroep, ComplexgroepAdmin)
admin.site.register(Gebrek)
admin.site.register(Conditiefoto)