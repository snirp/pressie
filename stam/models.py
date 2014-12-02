from django.core.urlresolvers import reverse
from django.db import models

ERNST_KEUZES = (
    (1, 'Gering'),
    (2, 'Serieus'),
    (3, 'Ernstig'),
)


INTENSITEIT_KEUZES = (
    (1, 'Laag'),
    (2, 'Midden'),
    (3, 'Hoog'),
)

EENHEID_KEUZES = (
    (1, '%'),
    (2, 'm'),
    (3, 'm2'),
    (5, 'st'),
    (6, 'won'),
    (7, 'vd')
)


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


class Activiteit(models.Model):
    naam = models.CharField(max_length=80)
    normprijs = models.DecimalField(max_digits=8, decimal_places=2)
    eenheid = models.IntegerField(choices=EENHEID_KEUZES)
    btw = models.DecimalField(max_digits=4, decimal_places=2) #slimmer systeem?

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['naam']
        verbose_name_plural = 'Activiteiten'


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

    def __str__(self):
        return self.naam

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

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['codering', 'naam']
        verbose_name_plural = 'Elementen'


class Hoofdgroep(models.Model):
    naam = models.CharField(max_length=50)
    order = models.IntegerField()
    standaard_elementen = models.ManyToManyField(Element, null=True, blank=True)
    stravis_hoofdgroep = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.naam

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Hoofdgroepen'