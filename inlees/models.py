from django.db import models
from onderhoud.models import Hoofdgroep, Element, Nengebrek, Activiteit, Gebrektype, Conditiedeel, Deel, Complex, \
    Conditiemeting, Scenario


class StravisDatabase(models.Model):
    naam = models.CharField(max_length=20)

    def __str__(self):
        return self.naam


# # # Stravis sleutels voor synchronisatie en import # # #

class DeelcomplexLink(models.Model):
    complex = models.OneToOneField(Complex)
    database = models.ForeignKey(StravisDatabase)
    deelcomplex_stravis = models.PositiveIntegerField()

    def __str__(self):
        return self.complex.__str__()


class ScenarioLink(models.Model):
    scenario = models.OneToOneField(Scenario)
    database = models.ForeignKey(StravisDatabase)
    scenario_stravis = models.PositiveIntegerField()

    def __str__(self):
        return self.scenario.__str__()


class ConditiemetingLink(models.Model):
    conditiemeting = models.OneToOneField(Conditiemeting)
    database = models.ForeignKey(StravisDatabase)
    conditiemeting_stravis = models.PositiveIntegerField()

    def __str__(self):
        return self.conditiemeting.__str__()


class ConditiedeelLink(models.Model):
    conditiedeel = models.OneToOneField(Conditiedeel)
    database = models.ForeignKey(StravisDatabase)
    deel_stravis = models.PositiveIntegerField()

    def __str__(self):
        return self.conditiedeel.__str__()


class DeelLink(models.Model):
    deel = models.OneToOneField(Deel)
    database = models.ForeignKey(StravisDatabase)
    scenariodeel_stravis = models.PositiveIntegerField()

    def __str__(self):
        return self.deel.__str__()


# # # Vertaaltabellen # # #


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


class ImportScenario(models.Model):
    sc_stravis = models.PositiveIntegerField()
    sc_start = models.PositiveIntegerField()
    sc_naam = models.CharField(max_length=80)
    dc_stravis = models.PositiveIntegerField()
    dc_code = models.CharField(max_length=20)
    dc_naam = models.CharField(max_length=60)
    dc_functie = models.CharField(max_length=40, null=True, blank=True)
    dc_aantal_eh = models.PositiveIntegerField(null=True, blank=True)
    dc_bouwjaar = models.PositiveIntegerField(null=True, blank=True)
    dc_straat = models.CharField(max_length=80, null=True, blank=True)
    dc_huisnummer = models.CharField(max_length=20, null=True, blank=True)
    dc_plaats = models.CharField(max_length=60, null=True, blank=True)
    cm_stravis = models.PositiveIntegerField(null=True, blank=True)
    cm_datum = models.DateField(null=True, blank=True)


class ImportDeel(models.Model):
    deel_stravis = models.PositiveIntegerField(null=True, blank=True)
    scenariodeel_stravis = models.PositiveIntegerField()
    hoofdgroep_stravis = models.PositiveIntegerField()
    naam = models.CharField(max_length=130)
    schilderjaar = models.PositiveIntegerField(null=True, blank=True)
    vervangjaar = models.PositiveIntegerField(null=True, blank=True)
    hvh_sw = models.FloatField(null=True, blank=True)
    hvh_ogr = models.FloatField(null=True, blank=True)
    element_stravis = models.PositiveIntegerField()
    eh_sw = models.PositiveIntegerField(null=True, blank=True)  # fallback naar generiek element
    eh_ogr = models.PositiveIntegerField() # fallback naar generiek element
    conditie_sw = models.PositiveIntegerField(null=True, blank=True)
    conditie_ogr = models.PositiveIntegerField(null=True, blank=True)
    sc_stravis = models.PositiveIntegerField(null=True, blank=True)
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
    eh_prijs_excl = models.DecimalField(max_digits=10, decimal_places=2)
    eh_prijs_incl = models.DecimalField(max_digits=10, decimal_places=2)
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