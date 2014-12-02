from decimal import Decimal
from django.core.urlresolvers import reverse
from django.db import models
from stam.models import Hoofdgroep, Element, Activiteit, Nengebrek, INTENSITEIT_KEUZES

CONDITIE_KEUZES = list(zip(range(1, 7), range(1, 7)))

OMVANG_KEUZES = (
    (0, '< 2%'),
    (1, '2% tot 10%'),
    (2, '10% tot 30%'),
    (3, '30% tot 70%'),
    (4, '> 70%'),
)

# # # # # Complexgegevens # # # # #


class Complex(models.Model):
    naam = models.CharField(max_length=60)
    code = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='complex', null=True, blank=True)
    actueel_scenario = models.OneToOneField('Scenario', related_name="actueel", null=True, blank=True)

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

    def __str__(self):
        return self.hoofdgroep.__str__()

    class Meta:
        ordering = ['hoofdgroep']
        verbose_name_plural = 'Complexgroepen'


class Complexdeel(models.Model):
    element = models.ForeignKey(Element, null=True, blank=True) #TODO elementen invullen, dan niet-optioneel
    complexgroep = models.ForeignKey(Complexgroep)
    onderhoudsjaar = models.IntegerField()
    # onderhoudshistorie

    def __str__(self):
        return self.element.__str__()

    def complex_naam(self):
        return self.complexgroep.complex.__str__()

    class Meta:
        ordering = ['complexgroep', 'element']
        verbose_name_plural = 'Complexdelen'


# # # # # Scenariogegevens # # # # #


class Scenario(models.Model):
    naam = models.CharField(max_length=80)
    start = models.IntegerField()
    eind = models.IntegerField()
    complex = models.ForeignKey(Complex)

    def __str__(self):
        return self.naam

    def jaar_bereik(self):
        return range(self.start, self.eind + 1)

    def restbereik_beschrijving(self, detail_bereik=10):
        if detail_bereik >= len(self.jaar_bereik()):
            return None
        elif detail_bereik == len(self.jaar_bereik()) + 1:
            # speciaal geval, er is maar 1 restjaar
            return self.jaar_bereik()[-1]
        else:
            # return "2025-2039"
            rest_bereik = self.jaar_bereik()[detail_bereik:]
            return "{}-{}".format(rest_bereik[0], rest_bereik[-1])

    def jaarbedragen(self, jaar_bereik=None):
        # Som van onderliggende maatregelkosten voor elk van de jaren in bereik
        if not jaar_bereik:
            jaar_bereik = self.jaar_bereik()
        sgrp_jaarbedragen = [sgrp.jaarbedragen(jaar_bereik=jaar_bereik) for sgrp in self.scenariogroep_set.all()]
        return [sum(i) for i in zip(*sgrp_jaarbedragen)]

    def detailbedragen(self, detail_bereik=10):
        # Som van de onderliggende maatregelkosten voor de eerste X jaar
        self.jaarbedragen(self.jaar_bereik()[:detail_bereik])

    def restbereik_bedrag(self, detail_bereik=10):
        return sum([sgrp.restbereik_bedrag(detail_bereik=detail_bereik) for sgrp in self.scenariogroep_set.all()])



class Scenariogroep(models.Model):
    complexgroep = models.ForeignKey(Complexgroep)
    scenario = models.ForeignKey(Scenario)
    # what else?

    def __str__(self):
        return self.complexgroep.__str__()

    def jaarbedragen(self, jaar_bereik=None):  # TODO gebruik jaarbedragen methode van onderliggende delen
        # Som van onderliggende maatregelkosten voor elk van de jaren in bereik
        if not jaar_bereik:
            jaar_bereik = self.scenario.jaar_bereik()
        maatregel_jaren = []
        for d in self.deel_set.all():
            for m in d.maatregel_set.all():
                maatregel_jaren.append(m.jaarbedragen(jaar_bereik))
        return [sum(i) for i in zip(*maatregel_jaren)]
        #List is unpacked, zipped and summed

    def detailbedragen(self, detail_bereik=10):
        # Som van de onderliggende maatregelkosten voor de eerste X jaar
        self.jaarbedragen(self.scenario.jaar_bereik()[:detail_bereik])

    def restbereik_bedrag(self, detail_bereik=10):
        restbedrag = 0
        for d in self.deel_set.all():
            for m in d.maatregel_set.all():
                restbedrag += m.restbereik_bedrag(detail_bereik=detail_bereik)
        return restbedrag

    class Meta:
        ordering = ['complexgroep']
        verbose_name_plural = 'Scenariogroepen'


class Deel(models.Model):
    naam = models.CharField(max_length=80)
    complexdeel = models.ForeignKey(Complexdeel)
    scenariogroep = models.ForeignKey(Scenariogroep)
    hvh = models.FloatField()
    stravis_scdeel = models.IntegerField(null=True, blank=True)  # scenariodeel

    def __str__(self):
        return self.naam

    def get_eenheid(self):
        return self.complexdeel.element.get_eenheid_display()

    class Meta:
        ordering = ['scenariogroep', 'naam']
        verbose_name_plural = 'Delen'


class Maatregel(models.Model):
    naam = models.CharField(max_length=80)
    activiteit = models.ForeignKey(Activiteit)
    ehprijs = models.DecimalField(max_digits=8, decimal_places=2)
    relatief = models.BooleanField(default=False)
    hvh = models.FloatField(default=100)
    start = models.IntegerField()
    cyclus = models.IntegerField()
    eind = models.IntegerField()
    opmerking = models.CharField(max_length=200, null=True, blank=True)
    stravis_scnmr = models.IntegerField(null=True, blank=True)  # scenario normmaatregel
    deel = models.ForeignKey(Deel)

    def __str__(self):
        return self.naam

    def hvh_display(self):
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

    def kosten_ex(self):
        return self.ehprijs * Decimal(str(self.q()))

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

    def jaarbedragen(self, jaar_bereik=None):
        if not jaar_bereik:
            jaar_bereik = self.deel.scenariogroep.scenario.jaar_bereik()
        # Jaarbedrag (0 of kosten) voor ieder jaar in bereik
        start, cyclus, eind, kosten = self.start, self.cyclus, self.eind, self.kosten_ex()
        return [kosten if self.__uitvoerjaar(jaar, start, eind, cyclus) else 0 for jaar in jaar_bereik]

    def restbereik_bedrag(self, detail_bereik=10, totaal_bereik=None):
        """
        In een scenario-weergave kan in het totale bereik onderscheid gemaakt worden tussen een detail-bereik
        en een rest-bereik. Deze functie geeft voor het rest-bereik een totaalbedrag over de resterende jaren.

        Bijvoorbeeld: scenario over 15 jaar met 10 detail jaren. De bedragen van de laatse 5 jaar worden dan
        gesommeerd in het restbereik-bedrag.
        """
        if not totaal_bereik:
            totaal_bereik = self.deel.scenariogroep.scenario.jaar_bereik()
        if detail_bereik > len(totaal_bereik):
            # Geen restjaren om weer te geven
            return None
        return sum(self.jaarbedragen(totaal_bereik[detail_bereik:]))

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

    class Meta:
        verbose_name_plural = 'Gebreken'


class Conditiefoto(models.Model):
    foto = models.ImageField(upload_to='images')
    conditiedeel = models.ForeignKey(Conditiedeel)


