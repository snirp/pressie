import csv
from io import StringIO
import decimal
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django import forms
import zipfile
from inlees.models import ImportDeel, ImportMaatregel, ImportGebrek, VertaalHoofdgroep, VertaalElement, \
    ConditiedeelLink, DeelLink, VertaalGebrek, VertaalGebrektype, VertaalActiviteit
from onderhoud.models import Scenario, Complexgroep, Scenariogroep, Conditiegroep, Complexdeel, Deel, \
    Conditiedeel, Gebrek, Maatregel, Nengebrek, Activiteit, Element


class UploadFileForm(forms.Form):
    file = forms.FileField()

"""
Upload take place through a single zip file containing .CSV files with records.

In order to rebuild relationships a stravis_id, corresponding with the original
database ID, is added for various entities. This is done via a OneToOne relationship.

"""

# The CSV uses a comma as decimal separator and consequently csvreader places single quotes around every value.
# These "convert" functions take care of proper conversion, especially with empty values.

def convert_integer(val):
    try:
        return int(val)
    except ValueError:
        return None


def convert_float(val):
    try:
        return float(val.replace(',', '.'))
    except ValueError:
        return None


def convert_decimal(val):
    try:
        return decimal.Decimal(val.replace(',', '.'))
    except ValueError:
        return None


def convert_bool(val):
    try:
        return 1 == int(val)
    except ValueError:
        return None


def import_data(uploadfile):
    zf = zipfile.ZipFile(uploadfile, 'r')
    # Dump the CSV contents to tables for further processing
    data = StringIO(zf.read("import_deel.csv").decode("utf-8"))
    reader = csv.reader(data)
    for r in reader:
        impd = ImportDeel(
            deel_stravis=convert_integer(r[0]),
            scenariodeel_stravis=convert_integer(r[1]),
            hoofdgroep_stravis=convert_integer(r[2]),
            naam=r[3],
            schilderjaar=convert_integer(r[4]),
            vervangjaar=convert_integer(r[5]),
            hvh_sw=convert_float(r[6]),
            hvh_ogr=convert_float(r[7]),
            element_stravis=convert_integer(r[8]),
            eh_sw=convert_integer(r[9]),
            eh_ogr=convert_integer(r[10]),
            conditie_sw=convert_integer(r[11]),
            conditie_ogr=convert_integer(r[12])
        )
        impd.save()

    data = StringIO(zf.read("import_maatregel.csv").decode("utf-8"))
    reader = csv.reader(data)
    for r in reader:
        impm = ImportMaatregel(
            scenariomaatregel_stravis=convert_integer(r[0]),
            scenariodeel_stravis=convert_integer(r[1]),
            activiteit_stravis=convert_integer(r[2]),
            eenheid=convert_integer(r[3]),
            naam=r[4],
            eh_prijs_excl=convert_decimal(r[5]),
            eh_prijs_incl=convert_decimal(r[6]),
            relatief=convert_bool(r[7]),
            hvh_uitvoer=convert_float(r[8])/100,  # Divide by 100% when coming from Stravis
            start=convert_integer(r[9]),
            cyclus=convert_integer(r[10]),
            eind=convert_integer(r[11]),
            opmerking=''  # TODO fix export om opmerking mee te nemen
        )
        impm.save()

    data = StringIO(zf.read("import_gebrek.csv").decode("utf-8"))
    reader = csv.reader(data)
    for r in reader:
        impg = ImportGebrek(
            gemeten_stravis=convert_integer(r[0]),
            deel_stravis=convert_integer(r[1]),
            gebrek_stravis=convert_integer(r[2]),
            gebrektype=convert_integer(r[3]),
            naam=r[4],
            omvang=convert_integer(r[5]),
            intensiteit=convert_integer(r[6])
        )
        impg.save()


def build_scenario(s):
    for ideel in ImportDeel.objects.all():
        # # # Complexgroep # # #
        hg = VertaalHoofdgroep.objects.get(hoofdgroep_stravis=ideel.hoofdgroep_stravis).hoofdgroep
        cxg, created = Complexgroep.objects.get_or_create(
            complex=s.complex,
            hoofdgroep=hg,
            naam=hg.naam
        )
        if created:
            cxg.save()

        # # # Complexdeel # # #
        try:
            cxd_element = VertaalElement.objects.get(element_stravis=ideel.element_stravis).element
        except ObjectDoesNotExist:
            e_eh = ideel.eh_sw or ideel.eh_ogr
            cxd_element = Element.objects.get(generiek=True, eenheid=e_eh)

        cxd_ohjaar = ideel.schilderjaar or ideel.vervangjaar

        cd = Complexdeel(
            element=cxd_element,
            complexgroep=cxg,
            onderhoudsjaar=cxd_ohjaar
        )
        cd.save()

        # # # Scenariogroep # # #
        sg, created = Scenariogroep.objects.get_or_create(
            complexgroep=cxg,
            scenario=s
        )
        if created:
            sg.save()

        # # # Deel # # #
        try:
            d_omreken = VertaalElement.objects.get(element_stravis=ideel.element_stravis).omrekenfactor
        except ObjectDoesNotExist:
            d_omreken = 1
        # Kuis de naam van het deel:
        # 1. Verwijder blanco soort en materiaal aanduiding ("- ");
        # 2. Verwijder eventuele Stravis hoofdgroepaanduiding;
        # 3. Eerste letter een hoofdletter.
        d_naam = ideel.naam.replace(' -', '')
        shg_prefix = VertaalHoofdgroep.objects.get(hoofdgroep_stravis=ideel.hoofdgroep_stravis).naam_stravis
        if d_naam.startswith(shg_prefix):
            d_naam = d_naam[len(shg_prefix)+1:]
        d_naam = d_naam.capitalize()

        d_hvh = ideel.hvh_sw * d_omreken or ideel.hvh_ogr * d_omreken

        d = Deel(
            naam=d_naam,
            complexdeel=cd,
            scenariogroep=sg,
            hvh=d_hvh
        )
        d.save()

        # # # Deel Link # # #
        dlink = DeelLink(
            deel=d,
            scenariodeel_stravis=ideel.scenariodeel_stravis
        )
        dlink.save()

        # # # Conditiegroep # # #
        cg, created = Conditiegroep.objects.get_or_create(
            conditiemeting=s.conditiemeting,
            scenariogroep=sg
        )
        if created:
            cg.save()

        # # # Conditiedeel # # #
        cd_score = max(ideel.conditie_sw, ideel.conditie_ogr)
        cd = Conditiedeel(
            conditiegroep=cg,
            deel=d,
            conditiescore=cd_score
        )
        cd.save()

        # # # Conditiedeel Link # # #
        if ideel.deel_stravis:
            cdlink = ConditiedeelLink(
                conditiedeel=cd,
                deel_stravis=ideel.deel_stravis
            )
            cdlink.save()

    # # # Gebrek # # #
    for igebrek in ImportGebrek.objects.all():
        cd = ConditiedeelLink.objects.get(deel_stravis=igebrek.deel_stravis).conditiedeel
        # Vind matchend gebrek in vertaaltabel of val terug naar generiek gebrek
        # Het generieke gebrek dient van gelijk gebrektype te zijn.
        try:
            ng = VertaalGebrek.objects.get(gebrek_stravis=igebrek.gebrek_stravis).nengebrek
        except ObjectDoesNotExist:
            gtype = VertaalGebrektype.objects.get(gebrektype_stravis=igebrek.gebrektype).gebrektype
            ng = Nengebrek.objects.get(generiek=True, gebrektype=gtype)

        g = Gebrek(
            naam=igebrek.naam,
            omvang=igebrek.omvang,
            intensiteit=igebrek.intensiteit,
            conditiedeel=cd,
            nengebrek=ng
        )
        g.save()

    # # # Maatregel # # #
    for imr in ImportMaatregel.objects.all():
        d = DeelLink.objects.get(scenariodeel_stravis=imr.scenariodeel_stravis).deel
        # Vind matchende activiteit in vertaaltabel of val terug naar generieke activiteit
        # De generieke activiteit dient een gelijke eenheid te hebben.
        try:
            act = VertaalActiviteit.objects.get(activiteit_stravis=imr.activiteit_stravis).activiteit
        except ObjectDoesNotExist:
            act = Activiteit.objects.get(generiek=True, eenheid=imr.eenheid)

        btw = (imr.eh_prijs_incl - imr.eh_prijs_excl) / imr.eh_prijs_excl

        m = Maatregel(
            naam=imr.naam.capitalize(),
            activiteit=act,
            btw_percentage=btw,
            ehprijs_excl=imr.eh_prijs_excl,
            relatief=imr.relatief,
            hvh=imr.hvh_uitvoer,
            start=imr.start,
            cyclus=imr.cyclus,
            # eind=imr.eind,
            # infinite cycle by default
            opmerking=imr.opmerking,
            deel=d
        )
        m.save()

    # Clear tables after import is processed
    ImportDeel.objects.all().delete()
    ImportMaatregel.objects.all().delete()
    ImportGebrek.objects.all().delete()



def zip_upload(request, pk):
    s = Scenario.objects.get(pk=pk)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            import_data(request.FILES['file'])
            build_scenario(s)
            return HttpResponseRedirect('/upload_successful')
    else:
        form = UploadFileForm()
    context = {'form': form, 's': s}
    context.update(csrf(request))
    return render_to_response('inlees/upload.html', context)
