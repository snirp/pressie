from django.contrib import admin
from gebouw.models import Complex, Complexgroep, Complexdeel, Scenario, Scenariogroep, Deel, Maatregel, \
    Conditiemeting, Conditiegroep, Conditiedeel, Gebrek, Conditiefoto


class ComplexgroepInline(admin.TabularInline):
    model = Complexgroep


class ComplexAdmin(admin.ModelAdmin):
    inlines = [ComplexgroepInline]
    list_display = ('code', 'naam',)


class ScenariogroepInline(admin.TabularInline):
    model = Scenariogroep


class ScenarioAdmin(admin.ModelAdmin):
    inlines = [ScenariogroepInline]
    list_display = ('complex', 'naam', 'start', 'eind')


class ConditiegroepInline(admin.TabularInline):
    model = Conditiegroep


class ConditiemetingAdmin(admin.ModelAdmin):
    inlines = [ConditiegroepInline]
    list_display = ('complex_naam', 'datum', 'scenario')


class ComplexdeelAdmin(admin.ModelAdmin):
    list_display = ('element', 'complexgroep', 'complex_naam')


class DeelAdmin(admin.ModelAdmin):
    list_display = ('naam', 'hvh')


class GebrekInline(admin.TabularInline):
    model = Gebrek


class ConditiefotoInline(admin.TabularInline):
    model = Conditiefoto


class ConditiedeelAdmin(admin.ModelAdmin):
    inlines = [GebrekInline, ConditiefotoInline]
    list_display = ('conditiegroep', 'deel', 'conditiescore', 'get_complex_str', 'get_conditiemeting_str' )
    list_filter = ('conditiescore', )


class MaatregelAdmin(admin.ModelAdmin):
    list_display = ('naam', 'hvh', 'eh', 'ehprijs', 'start', 'cyclus', 'eind')

admin.site.register(Complex, ComplexAdmin)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Conditiemeting, ConditiemetingAdmin)
admin.site.register(Complexdeel, ComplexdeelAdmin)
admin.site.register(Deel, DeelAdmin)
admin.site.register(Conditiedeel, ConditiedeelAdmin)
admin.site.register(Maatregel, MaatregelAdmin)

admin.site.register(Scenariogroep)



admin.site.register(Conditiegroep)

admin.site.register(Gebrek)
admin.site.register(Conditiefoto)