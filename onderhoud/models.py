from datetime import date
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from onderhoud.nenhelp import calculate_aggregated, calculate_conditie, calculate_gebrek

ERNST_KEUZES = (
    (1, 'Gering'),
    (2, 'Serieus'),
    (3, 'Ernstig'),
)

INTENSITEIT_KEUZES = (
    (0, 'Laag'),
    (1, 'Midden'),
    (2, 'Hoog'),
)

EENHEID_KEUZES = (
    (1, '%'),
    (2, 'm'),
    (3, 'm2'),
    (5, 'st'),
    (6, 'won'),
    (7, 'verd'),
    (8, 'zijde'),
    (9, 'post'),
)

CONDITIE_KEUZES = list(zip(range(1, 7), range(1, 7)))

OMVANG_KEUZES = (
    (0, '< 2%'),
    (1, '2% tot 10%'),
    (2, '10% tot 30%'),
    (3, '30% tot 70%'),
    (4, '> 70%'),
)

OMVANG_WAARDES = (0.01, 0.06, 0.2, 0.5, 0.9)
INTENSITEIT_WAARDES = ('laag', 'midden', 'hoog')
ERNST_WAARDES = ('dummy0', 'gering', 'serieus', 'ernstig')


# # # STAMGEGEVENS # # #


class Hoofdcodering(models.Model):
    code = models.IntegerField()
    naam = models.CharField(max_length=50)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Hoofdcoderingen'


class Codering(models.Model):
    code = models.CharField(max_length=4)
    naam = models.CharField(max_length=60)
    hoofdcodering = models.ForeignKey(Hoofdcodering)

    def __str__(self):
        return self.code

    def lang(self):
        return "{}.{}".format(self.hoofdcodering.__str__(), self.naam)

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Coderingen'


class Btw(models.Model):
    naam = models.CharField(max_length=20)
    percentage = models.FloatField()

    def __str__(self):
        return self.naam


class Deelactiviteit(models.Model):
    btw = models.ForeignKey(Btw)
    naam = models.CharField(max_length=80)
    beschrijving = models.TextField(null=True, blank=True)
    eh_prijs = models.DecimalField(max_digits=8, decimal_places=2)
    eenheid = models.IntegerField(choices=EENHEID_KEUZES)

    def __str__(self):
        return self.naam


class Activiteit(models.Model):
    naam = models.CharField(max_length=80)
    eenheid = models.IntegerField(choices=EENHEID_KEUZES)
    generiek = models.BooleanField(default=False)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'Activiteiten'


class ActiviteitOnderbouwing(models.Model):
    activiteit = models.ForeignKey(Activiteit)
    deelactiviteit = models.ForeignKey(Deelactiviteit)
    hoeveelheid = models.FloatField(default=1.0)


class Gebrektype(models.Model):
    naam = models.CharField(max_length=50)
    ernst = models.IntegerField(choices=ERNST_KEUZES)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['-ernst', 'naam']


class Nengebrek(models.Model):
    naam = models.CharField(max_length=60)
    gebrektype = models.ForeignKey(Gebrektype)
    generiek = models.BooleanField(default=False)

    def __str__(self):
        return self.naam

    def clean(self):
        if self.generiek:
            try:
                duplicate = Nengebrek.objects.exclude(pk=self.pk).get(gebrektype=self.gebrektype, generiek=True)
                raise ValidationError('Generiek gebrek van type "{}" bestaat reeds.'.format(self.gebrektype.__str__()))
            except Nengebrek.DoesNotExist:
                pass

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'Nengebreken'


class Element(models.Model):
    naam = models.CharField(max_length=60)
    codering = models.ForeignKey(Codering)
    eenheid = models.IntegerField(choices=EENHEID_KEUZES)
    standaard_activiteiten = models.ManyToManyField(Activiteit, null=True, blank=True)
    standaard_gebreken = models.ManyToManyField(Nengebrek, null=True, blank=True)
    vervangwaarde = models.PositiveIntegerField(default=1)
    steekwoorden = models.CharField(max_length=100, null=True, blank=True)
    omschrijving = models.TextField(null=True, blank=True)
    generiek = models.BooleanField(default=False)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'Elementen'


class Hoofdgroep(models.Model):
    naam = models.CharField(max_length=50)
    order = models.IntegerField()
    standaard_elementen = models.ManyToManyField(Element, null=True, blank=True)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Hoofdgroepen'


# # # # # COMPLEXGEGEVENS # # # # #


class Complex(models.Model):
    naam = models.CharField(max_length=60)
    code = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='complex', null=True, blank=True)
    actueel_scenario = models.OneToOneField('Scenario', related_name="actueel", null=True, blank=True)
    admin = models.ForeignKey(User, null=True, blank=True, related_name="complexadmin")
    eenheden = models.PositiveIntegerField(null=True, blank=True)
    bouwjaar = models.PositiveIntegerField(null=True, blank=True)
    straat = models.CharField(max_length=80, null=True, blank=True)
    huisnummer = models.CharField(max_length=20, null=True, blank=True)
    plaats = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.naam

    def get_absolute_url(self):
        return reverse('complex_detail', args=(self.id,))

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Complexen'


class Complexgroep(models.Model):
    complex = models.ForeignKey(Complex)
    hoofdgroep = models.ForeignKey(Hoofdgroep)
    beschrijving = models.TextField(null=True, blank=True)
    naam = models.TextField(max_length=80)  # ? default hoofdgroep naam (bij save method) ?

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['complex', 'hoofdgroep']
        verbose_name_plural = 'Complexgroepen'


class Complexdeel(models.Model):
    element = models.ForeignKey(Element)
    complexgroep = models.ForeignKey(Complexgroep)
    onderhoudsjaar = models.IntegerField(null=True, blank=True)
    # onderhoudshistorie

    def __str__(self):
        return self.element.__str__()

    def complex_naam(self):
        return self.complexgroep.complex.__str__()

    class Meta:
        ordering = ['complexgroep', 'element']
        verbose_name_plural = 'Complexdelen'


# # # # # SCENARIO # # # # #


class Scenario(models.Model):
    naam = models.CharField(max_length=80)
    start = models.IntegerField(default=date.today().year + 1)
    complex = models.ForeignKey(Complex)

    def __str__(self):
        return self.naam

    def get_begroting_url(self):
        return reverse('begroting', args=(self.id,))



    """
    def begroting_bereik(self, bereik=25):
        return range(self.start, self.start + bereik)

    def restbereik_beschrijving(self, bereik=25, detail_bereik=10):
        if detail_bereik >= bereik:
            return None
        elif detail_bereik == bereik - 1:
            return self.begroting_bereik(bereik)[-1]
        else:
            rest_bereik = self.begroting_bereik(bereik)[detail_bereik:]
            return "{}-{}".format(rest_bereik[0], rest_bereik[-1])

    def jaarbedragen(self, jaar_bereik=None, btw=None):
        # Som van onderliggende maatregelkosten voor elk van de jaren in bereik
        if not jaar_bereik:
            jaar_bereik = self.begroting_bereik()
        sgrp_jaarbedragen = [sgrp.jaarbedragen_incl(jaar_bereik=jaar_bereik) for sgrp in self.scenariogroep_set.all()]
        return [sum(i) for i in zip(*sgrp_jaarbedragen)]

    def detailbedragen(self, detail_bereik=10):
        # Som van de onderliggende maatregelkosten voor de eerste X jaar
        self.jaarbedragen(self.jaar_bereik()[:detail_bereik])

    def restbereik_bedrag_incl(self, detail_bereik=10):
        return sum([sgrp.restbereik_bedrag_incl(detail_bereik=detail_bereik) for sgrp in self.scenariogroep_set.all()])
    """


class Scenariogroep(models.Model):
    complexgroep = models.ForeignKey(Complexgroep)
    scenario = models.ForeignKey(Scenario, related_name='scenariogroepen')
    # what else?

    def naam(self):
        #alias for API use
        return self.__str__()

    def __str__(self):
        return self.complexgroep.__str__()

    """
    def jaarbedragen_incl(self, jaar_bereik=None):  # TODO gebruik jaarbedragen methode van onderliggende delen
        # Som van onderliggende maatregelkosten voor elk van de jaren in bereik
        if not jaar_bereik:
            jaar_bereik = self.scenario.jaar_bereik()
        maatregel_jaren = []
        for d in self.deel_set.all():
            for m in d.maatregel_set.all():
                maatregel_jaren.append(m.jaarbedragen_incl(jaar_bereik))
        return [sum(i) for i in zip(*maatregel_jaren)]
        #List is unpacked, zipped and summed

    def detailbedragen(self, detail_bereik=10):
        # Som van de onderliggende maatregelkosten voor de eerste X jaar
        self.jaarbedragen(self.scenario.jaar_bereik()[:detail_bereik])

    def restbereik_bedrag_incl(self, detail_bereik=10):
        restbedrag = 0
        for d in self.deel_set.all():
            for m in d.maatregel_set.all():
                restbedrag += m.restbereik_bedrag_incl(detail_bereik=detail_bereik)
        return restbedrag
    """

    class Meta:
        ordering = ['complexgroep']
        verbose_name_plural = 'Scenariogroepen'


class Deel(models.Model):
    naam = models.CharField(max_length=130)
    complexdeel = models.ForeignKey(Complexdeel)
    scenariogroep = models.ForeignKey(Scenariogroep, related_name='delen')
    hvh = models.FloatField()
    start = models.PositiveIntegerField(null=True, blank=True)
    eind = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.naam

    def eenheid(self):
        return self.complexdeel.element.get_eenheid_display()

    def get_scenario(self):
        return self.scenariogroep.scenario.__str__()

    class Meta:
        ordering = ['scenariogroep', 'naam']
        verbose_name_plural = 'Delen'


class Maatregel(models.Model):
    naam = models.CharField(max_length=80)
    activiteit = models.ForeignKey(Activiteit)
    btw_percentage = models.FloatField()
    ehprijs_excl = models.DecimalField(max_digits=8, decimal_places=2)
    relatief = models.BooleanField(default=False)
    hvh = models.FloatField(default=100)
    start = models.PositiveIntegerField(default=date.today().year + 1)
    cyclus = models.PositiveIntegerField(null=True, blank=True)
    eind = models.PositiveIntegerField(null=True, blank=True)
    opmerking = models.TextField(null=True, blank=True)
    deel = models.ForeignKey(Deel, related_name='maatregelen')

    def __str__(self):
        return self.naam

    def hoeveelheid(self):
        # display logic: consider implementing as a template tag instead
        if self.relatief:
            return self.hvh * 100
        else:
            return self.hvh

    def eh(self):
        # percentage of eenheid van activiteit
        if self.relatief:
            return "%"
        else:
            return self.activiteit.get_eenheid_display()

    def q(self):
        # kwantiteit van uitvoering
        if self.relatief:
            return self.hvh * self.deel.hvh
        else:
            return self.hvh

    def prijs_excl(self):
        return Decimal(self.q()) * self.ehprijs_excl

    """
    def kosten_excl(self):
        return self.ehprijs_excl * Decimal(str(self.q()))

    def kosten_incl(self):
        return self.ehprijs_incl * Decimal(str(self.q()))

    @staticmethod
    def __uitvoerjaar(jaar, start, eind, cyclus):
        # Controleer of het jaar een geldig uitvoerjaar in de cyclus is.
        if jaar == start:
            return True
        elif cyclus == 0:
            return False
        elif not (jaar-start)/cyclus % 1 and jaar <= eind:
            return True
        else:
            return False

    def jaarbedragen_incl(self, jaar_bereik=None):
        if not jaar_bereik:
            jaar_bereik = self.deel.scenariogroep.scenario.jaar_bereik()
        # Jaarbedrag (0 of kosten) voor ieder jaar in bereik
        start, cyclus, eind, kosten = self.start, self.cyclus, self.eind, self.kosten_incl()
        return [kosten if self.__uitvoerjaar(jaar, start, eind, cyclus) else 0 for jaar in jaar_bereik]

    def restbereik_bedrag_incl(self, detail_bereik=10, totaal_bereik=None):
        if not totaal_bereik:
            totaal_bereik = self.deel.scenariogroep.scenario.jaar_bereik()
        if detail_bereik > len(totaal_bereik):
            # Geen restjaren om weer te geven
            return None
        return sum(self.jaarbedragen_incl(totaal_bereik[detail_bereik:]))
    """

    class Meta:
        ordering = ['naam', 'start']
        verbose_name_plural = 'Maatregelen'


# # # # # Conditiegegevens # # # # #


class Conditiemeting(models.Model):
    datum = models.DateField()
    uitvoerder = models.CharField(max_length=80, null=True, blank=True)
    scenario = models.OneToOneField(Scenario, null=True, blank=True)

    def __str__(self):
        return self.datum.strftime('%c')

    def complex_naam(self):
        return self.scenario.complex.__str__()

    def complex_code(self):
        return self.scenario.complex.code

    def get_absolute_url(self):
        return reverse('conditiemeting_detail', args=(self.id,))

    def get_cmgroepen_url(self):
        return reverse('conditiemeting_groepen', args=(self.id,))

    class Meta:
        ordering = ['-datum']
        verbose_name_plural = 'Conditiemetingen'


class Conditiegroep(models.Model):
    scenariogroep = models.OneToOneField(Scenariogroep, null=True, blank=True)
    conditiemeting = models.ForeignKey(Conditiemeting)
    bevinding = models.TextField(null=True, blank=True)
    conditie = models.IntegerField(default=1, choices=CONDITIE_KEUZES)

    def __str__(self):
        return self.scenariogroep.__str__()

    def set_conditie(self):
        self.conditie = calculate_aggregated(self.conditiedeel_set.all())

    class Meta:
        ordering = ['scenariogroep']
        verbose_name_plural = 'Conditiegroepen'


class Conditiedeel(models.Model):
    deel = models.OneToOneField(Deel, null=True, blank=True)
    conditiegroep = models.ForeignKey(Conditiegroep)
    conditiescore = models.IntegerField(choices=CONDITIE_KEUZES)

    def __str__(self):
        return self.deel.__str__()

    def get_conditiemeting_str(self):
        return self.conditiegroep.conditiemeting.__str__()

    def get_complex_str(self):
        return self.conditiegroep.conditiemeting.scenario.complex.__str__()

    def get_gebreken_count(self):
        return self.gebrek_set.count()

    def set_conditie(self):
        self.conditiescore = calculate_conditie(self)

    class Meta:
        ordering = ['deel']
        verbose_name_plural = 'Conditiedelen'


class Gebrek(models.Model):
    naam = models.CharField(max_length=80)
    omvang = models.IntegerField(choices=OMVANG_KEUZES)
    intensiteit = models.IntegerField(choices=INTENSITEIT_KEUZES)
    conditiedeel = models.ForeignKey(Conditiedeel)
    nengebrek = models.ForeignKey(Nengebrek)

    def __str__(self):
        return self.naam

    def get_type(self):
        return self.nengebrek.gebrektype.__str__()

    def get_omvang_waarde(self):
        return OMVANG_WAARDES[self.omvang]

    def get_intensiteit_waarde(self):
        return INTENSITEIT_WAARDES[self.intensiteit]

    def get_ernst_waarde(self):
        return ERNST_WAARDES[self.nengebrek.gebrektype.ernst]

    def get_conditie(self):
        return calculate_gebrek(self)

    class Meta:
        verbose_name_plural = 'Gebreken'


class Conditiefoto(models.Model):
    foto = models.ImageField(upload_to='images')
    conditiedeel = models.ForeignKey(Conditiedeel)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('onderhoud.views.conditiefoto', args=[str(self.id)])
