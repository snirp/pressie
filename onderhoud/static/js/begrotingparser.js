
var parseBegroting = function(scenarioJson, horizon, detail, btw) {
    var startScenario = scenarioJson.start; // Startjaar van het scenario
    var rows = [];                          // Geordende array van row objects
    var detailKolommen = [];                // Array van detailjaren
    var restKolom = '';                     // Kolom header voor restkolom
    var isRest = horizon > detail + 1;        // wel of geen restjaren

    for (var i = 0; i < detail; i++) {
        detailKolommen.push(i + startScenario);
    }
    if (horizon > detail) {
        restKolom = (startScenario + detail) + '-' + (startScenario + horizon - 1);
    }

    // Helper functions for parsing

    var isUitvoerjaar = function(jaar, start, eind, cyclus) {
        // Bepaal of een bepaald jaar voor een gegeven start+eind+cyclus een uitvoerjaar is
        if (jaar == start) {
            return true
        } else if (!cyclus || jaar < start) {
            return false
        } else {
            return ( (jaar - start) / cyclus % 1 == 0 && ( jaar <= eind || !eind) );
        }
    };

    var jaarRij = function (bereikStart, duur, start, eind, cyclus, prijs) {
        // Geef voor elk jaar in een jaarbereik het bedrag, of 0 als het geen uitvoerjaar is
        var result = [];
        for (var y = bereikStart; y < (bereikStart + duur); y++) {
            if (isUitvoerjaar(y, start, eind, cyclus)) {
                result.push(prijs);
            } else {
                result.push(0);
            }
        }
        return result;
    };

    var kolomTotalen = function(arr) {
        // Geef voor een vierkante array een array met de kolomtotalen
        var result = [];
        for (var i = 0; i < arr.length; i++) {
            for (var j = 0; j < arr[i].length; j++) {
                result[j] = (result[j] || 0) + arr[i][j];
            }
        }
        return result;
    };

    // Main parsing loop

    for (var i = 0; i < scenarioJson.scenariogroepen.length; i++) {
        var sg = scenarioJson.scenariogroepen[i];
        for (var j = 0; j < sg.delen.length; j++) {
            var dl = sg.delen[j];
            for (var k = 0; k < dl.maatregelen.length; k++) {
                var mr = dl.maatregelen[k];

                // TODO implementeer rijobject met methodes
                var row = {};
                row.groep = sg.naam;
                row.deel = dl.naam;
                row.deelhvh = dl.hvh;
                row.deeleh = dl.eenheid;
                row.start = mr.start;
                row.cyclus = mr.cyclus || '';
                row.eind = mr.eind || '';
                row.btwPerc = mr.btw_percentage;
                row.ehprijs = (btw) ? (1 + row.btwPerc) * mr.ehprijs_excl: mr.ehprijs_excl;
                row.bedrag = (btw) ? (1 + row.btwPerc) * mr.prijs_excl: mr.prijs_excl;
                row.maatregel = mr.naam;
                row.uitvoerhvh = mr.hoeveelheid;
                row.uitvoereh = mr.eh;

                var detailArray = jaarRij(startScenario, detail, row.start, row.eind, row.cyclus, row.bedrag);
                for (var l = 0; l < detailArray.length; l++) {
                    row[detailKolommen[l]] = detailArray[l];
                }

                if (isRest){
                    var restArray = jaarRij(startScenario+detail, horizon-detail, row.start, row.eind, row.cyclus, row.bedrag);
                    row.restBedrag = restArray.reduce(function (prev, cur) {
                        return prev + cur;
                    });
                }
                detailArray.push(row.restBedrag);
                row.rijTotaal = detailArray.reduce(function (prev, cur) {
                        return prev + cur;
                    });
                rows.push(row);

            } // maatregel
        } // deel
    } // scenariogroep

    return {
        restKolom: restKolom,
        rows: rows,
        detailKolommen: detailKolommen
    }
};
