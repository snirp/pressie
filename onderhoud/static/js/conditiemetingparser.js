
var parseConditiemeting = function(cmJson) {
    var rows = [];

    for (var i = 0; i < cmJson.length; i++) {
        var cm = cmJson[i];
        for (var j = 0; j < cm.conditiegroep_set.length; j++) {
            var cg = cm.conditiegroep_set[j];
            for (var k = 0; k < cg.conditiedeel_set.length; k++) {
                var cd = cg.conditiedeel_set[k];
                for (var l = 0; l < cd.gebrek_set.length; l++) {
                    var gebrek = cd.gebrek_set[l];
                    var row = {};
                    row.complex = cm.complex_code + " " + cm.complex_naam;
                    row.datum = cm.datum;
                    row.conditiegroep = cg.__str__;
                    row.aggregatie = cg.conditie;
                    row.deel = cd.__str__;
                    row.conditie = cd.conditiescore;
                    row.gebrek = gebrek.naam;
                    row.gebrektype = gebrek.get_type;
                    row.gebrek = gebrek.naam;
                    row.omvang = gebrek.get_omvang_waarde;
                    row.intensiteit = gebrek.get_intensiteit_waarde;
                    row.ernst = gebrek.get_ernst_waarde;
                    rows.push(row);
                }
            }
        }
    }

    return rows;
};
