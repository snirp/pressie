import bisect

CORRECTIEFACTOR = {
    1: 1.0,
    2: 1.02,
    3: 1.1,
    4: 1.3,
    5: 1.7,
    6: 2.0
}
CONDITIELOOKUP = [0, 1.01, 1.04, 1.15, 1.4, 1.78]
OMVANGMAP = {
    0: 0.01,
    1: 0.06,
    2: 0.2,
    3: 0.5,
    4: 0.9
}
# Matrix dimensies: ERNST (3-1) -> OMVANG (0-4) -> INTENSITEIT (0-2)
CONDITIEMATRIX = {
    3: {
        0: {0: 1, 1: 1, 2: 2},
        1: {0: 1, 1: 2, 2: 3},
        2: {0: 2, 1: 3, 2: 4},
        3: {0: 3, 1: 4, 2: 5},
        4: {0: 4, 1: 5, 2: 6}
    },
    2: {
        0: {0: 1, 1: 1, 2: 1},
        1: {0: 1, 1: 1, 2: 2},
        2: {0: 1, 1: 2, 2: 3},
        3: {0: 2, 1: 3, 2: 4},
        4: {0: 3, 1: 4, 2: 5}
    },
    1: {
        0: {0: 1, 1: 1, 2: 1},
        1: {0: 1, 1: 1, 2: 1},
        2: {0: 1, 1: 1, 2: 2},
        3: {0: 1, 1: 2, 2: 3},
        4: {0: 2, 1: 3, 2: 4}
    }
}


def calculate_gebrek(gebrek):
    return CONDITIEMATRIX[gebrek.nengebrek.gebrektype.ernst][gebrek.omvang][gebrek.intensiteit]


def calculate_conditie(conditiedeel):
    gebreken = conditiedeel.gebrek_set.all()
    if not gebreken:
        return 1
    normaalomvang = 0
    conditieomvang = 0
    for g in gebreken:
        omvang = OMVANGMAP[g.omvang]
        normaalomvang += omvang
        conditieomvang += omvang * CORRECTIEFACTOR[calculate_gebrek(g)]
    return bisect.bisect_left(CONDITIELOOKUP, (conditieomvang/normaalomvang))


def calculate_aggregated(conditiedelen):
    normaalwaarde = 0
    conditiewaarde = 0

    for cd in conditiedelen:
        waarde = cd.deel.hvh * cd.deel.complexdeel.element.vervangwaarde
        normaalwaarde += waarde
        conditiewaarde += waarde * CORRECTIEFACTOR[cd.conditiescore]

    if not normaalwaarde:
        return 1
    return bisect.bisect_left(CONDITIELOOKUP, (conditiewaarde/normaalwaarde))



