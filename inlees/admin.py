from django.contrib import admin
from .models import StravisDatabase, VertaalActiviteit, VertaalElement, VertaalGebrek, VertaalHoofdgroep, \
    ImportGebrek, ImportMaatregel, ImportDeel, VertaalGebrektype, ImportScenario


admin.site.register(StravisDatabase)
admin.site.register(VertaalActiviteit)
admin.site.register(VertaalElement)
admin.site.register(VertaalGebrek)
admin.site.register(VertaalHoofdgroep)
admin.site.register(ImportScenario)
admin.site.register(ImportGebrek)
admin.site.register(ImportMaatregel)
admin.site.register(ImportDeel)
admin.site.register(VertaalGebrektype)
