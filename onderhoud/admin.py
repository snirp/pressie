from django.contrib import admin
from django.forms import ModelForm
from .models import Complex, Complexgroep, Complexdeel, Scenario, Scenariogroep, Deel, Maatregel, \
    Conditiemeting, Conditiegroep, Conditiedeel, Gebrek, Conditiefoto, Hoofdgroep, Hoofdcodering, Codering, \
    Element, Activiteit, Gebrektype, Nengebrek, Deelactiviteit, ActiviteitOnderbouwing, Btw


# Example to override queryset
class ConditiegroepAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConditiegroepAdminForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['scenariogroep'].queryset = Scenariogroep.objects.all()


class GebrekAdmin(admin.ModelAdmin):
    raw_id_fields = ('conditiedeel',)


class ConditiegroepAdmin(admin.ModelAdmin):
    raw_id_fields = ('scenariogroep',)
    #form = ConditiegroepAdminForm


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
    raw_id_fields = ('scenariogroep', )


class ConditiemetingAdmin(admin.ModelAdmin):
    inlines = [ConditiegroepInline]
    list_display = ('complex_naam', 'datum', 'scenario')


class ComplexdeelAdmin(admin.ModelAdmin):
    list_display = ('element', 'complexgroep')


class MaatregelInline(admin.TabularInline):
    model = Maatregel


class DeelAdmin(admin.ModelAdmin):
    list_display = ('scenariogroep', 'get_complex_naam', 'naam', 'hvh')
    inlines = [MaatregelInline]
    raw_id_fields = ('complexdeel', 'scenariogroep')


class GebrekInline(admin.TabularInline):
    model = Gebrek


class ConditiefotoInline(admin.TabularInline):
    model = Conditiefoto


class ConditiedeelAdmin(admin.ModelAdmin):
    inlines = [GebrekInline, ConditiefotoInline]
    list_display = ('conditiegroep', 'deel', 'conditiescore', 'get_complex_str', 'get_conditiemeting_str' )
    list_filter = ('conditiescore', )
    raw_id_fields = ('deel', 'conditiegroep')


class MaatregelAdmin(admin.ModelAdmin):
    list_display = ('naam', 'hvh', 'eh')


class DeelInline(admin.TabularInline):
    model = Deel
    raw_id_fields = ('complexdeel',)


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
admin.site.register(Conditiegroep, ConditiegroepAdmin)
admin.site.register(Complexgroep, ComplexgroepAdmin)
admin.site.register(Gebrek, GebrekAdmin)
admin.site.register(Conditiefoto)