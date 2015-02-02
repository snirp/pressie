from django.db import models
from onderhoud.models import Hoofdgroep, Element, Nengebrek, Activiteit, Gebrektype, Conditiedeel, Deel


class ConditiedeelLink(models.Model):
    # Stravis sleutel voor synchronisatie en import
    conditiedeel = models.OneToOneField(Conditiedeel)
    deel_stravis = models.PositiveIntegerField()

    def __str__(self):
        return self.conditiedeel.__str__()


class DeelLink(models.Model):
    # Stravis sleutel voor synchronisatie en import
    deel = models.OneToOneField(Deel)
    scenariodeel_stravis = models.PositiveIntegerField()

    def __str__(self):
        return self.deel.__str__()


class StravisDatabase(models.Model):
    naam = models.CharField(max_length=20)

    def __str__(self):
        return self.naam


class VertaalHoofdgroep(models.Model):
    hoofdgroep = models.ForeignKey(Hoofdgroep)
    hoofdgroep_stravis = models.PositiveIntegerField()
    database = models.ForeignKey(StravisDatabase)
    naam_stravis = models.CharField(max_length=80, null=True, blank=True)  # for trimming hoofdgroepnaam from deel naam

    def __str__(self):
        return self.hoofdgroep.__str__()

    class Meta:
        ordering = ['hoofdgroep_stravis']


class VertaalElement(models.Model):
    element = models.ForeignKey(Element)
    element_stravis = models.PositiveIntegerField()
    database = models.ForeignKey(StravisDatabase)
    omrekenfactor = models.FloatField(default=1.0)
    # op database + element_stravis een unique together constraint maken

    def __str__(self):
        return self.element.__str__()

    class Meta:
        verbose_name_plural = 'Vertaal Elementen'


class VertaalGebrek(models.Model):
    nengebrek = models.ForeignKey(Nengebrek)
    gebrek_stravis = models.PositiveIntegerField()
    database = models.ForeignKey(StravisDatabase)

    def __str__(self):
        return self.nengebrek.__str__()

    class Meta:
        verbose_name_plural = 'Vertaal gebreken'


class VertaalGebrektype(models.Model):
    gebrektype = models.OneToOneField(Gebrektype)
    gebrektype_stravis = models.PositiveIntegerField()
    database = models.ForeignKey(StravisDatabase)

    def __str__(self):
        return self.gebrektype.__str__()


class VertaalActiviteit(models.Model):
    activiteit = models.ForeignKey(Activiteit)
    activiteit_stravis = models.PositiveIntegerField()
    database = models.ForeignKey(StravisDatabase)

    def __str__(self):
        return self.activiteit.__str__()

    class Meta:
        verbose_name_plural = 'Vertaal activiteiten'


class ImportDeel(models.Model):
    deel_stravis = models.PositiveIntegerField(null=True, blank=True)
    scenariodeel_stravis = models.PositiveIntegerField()
    hoofdgroep_stravis = models.PositiveIntegerField()
    naam = models.CharField(max_length=80)
    schilderjaar = models.PositiveIntegerField(null=True, blank=True)
    vervangjaar = models.PositiveIntegerField(null=True, blank=True)
    hvh_sw = models.FloatField(null=True, blank=True)
    hvh_ogr = models.FloatField(null=True, blank=True)
    element_stravis = models.PositiveIntegerField()
    eh_sw = models.PositiveIntegerField(null=True, blank=True)  # fallback naar generiek element
    eh_ogr = models.PositiveIntegerField() # fallback naar generiek element
    conditie_sw = models.PositiveIntegerField(null=True, blank=True)
    conditie_ogr = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Import delen'


class ImportMaatregel(models.Model):
    scenariomaatregel_stravis = models.PositiveIntegerField()
    scenariodeel_stravis = models.PositiveIntegerField()
    activiteit_stravis = models.PositiveIntegerField()
    eenheid = models.PositiveIntegerField()  # fallback naar generieke activiteit
    naam = models.CharField(max_length=80)  # ook fallback
    eh_prijs_excl = models.DecimalField(max_digits=8, decimal_places=2)
    eh_prijs_incl = models.DecimalField(max_digits=8, decimal_places=2)
    relatief = models.BooleanField(default=True)
    hvh_uitvoer = models.FloatField()
    start = models.PositiveIntegerField()
    cyclus = models.PositiveIntegerField()
    eind = models.PositiveIntegerField()
    opmerking = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Import maatregelen'


class ImportGebrek(models.Model):
    gemeten_stravis = models.PositiveIntegerField()
    deel_stravis = models.PositiveIntegerField()
    gebrek_stravis = models.PositiveIntegerField()
    gebrektype = models.PositiveIntegerField()  # fallback naar generiek element
    naam = models.CharField(max_length=80)  # gebruiken indien generiek gebrek
    omvang = models.PositiveIntegerField()
    intensiteit = models.PositiveIntegerField()

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Import gebreken'