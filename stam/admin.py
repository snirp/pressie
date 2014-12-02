from django.contrib import admin
from stam.models import Hoofdgroep, Hoofdcodering, Codering, Element, Activiteit, Gebrektype, Nengebrek


class NengebrekAdmin(admin.ModelAdmin):
    list_display = ('naam', 'gebrektype', )


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


admin.site.register(Hoofdgroep)
admin.site.register(Hoofdcodering, HoofdcoderingAdmin)
admin.site.register(Codering, CoderingAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(Activiteit)
admin.site.register(Gebrektype)
admin.site.register(Nengebrek, NengebrekAdmin)
