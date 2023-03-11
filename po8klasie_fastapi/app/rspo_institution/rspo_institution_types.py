from enum import Enum


class RspoInstitutionTypeLevel1Generalization(Enum):
    SECONDARY_SCHOOL = "secondary_school"
    OTHER = "other"


class RspoInstitutionTypeLevel2Generalization(Enum):
    HIGH_SCHOOL = "high_school"
    TECHNICAL_HIGH_SCHOOL = "technical_high_school"
    VOCATIONAL_SCHOOL_LEVEL1 = "vocational_school_lvl1"
    VOCATIONAL_SCHOOL_LEVEL2 = "vocational_school_lvl2"
    OTHER = "other"


rspo_institution_types = {
    90: {
        "nazwa": "Bednarska Szkoła Realna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.SECONDARY_SCHOOL,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.HIGH_SCHOOL,
    },
    58: {"nazwa": "Biblioteki pedagogiczne"},
    93: {
        "nazwa": "Branżowa szkoła I stopnia",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.SECONDARY_SCHOOL,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.VOCATIONAL_SCHOOL_LEVEL1,
    },
    94: {
        "nazwa": "Branżowa szkoła II stopnia",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.SECONDARY_SCHOOL,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.VOCATIONAL_SCHOOL_LEVEL2,
    },
    55: {
        "nazwa": "Bursa",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    45: {
        "nazwa": "Centrum Kształcenia Praktycznego",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    96: {
        "nazwa": "Centrum Kształcenia Zawodowego",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    56: {
        "nazwa": "Dom wczasów dziecięcych",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    4: {
        "nazwa": "Gimnazjum",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    89: {
        "nazwa": "Inna szkoła artystyczna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    34: {
        "nazwa": "Kolegium nauczycielskie",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    65: {
        "nazwa": "Kolegium Pracowników Służb Społecznych",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    14: {
        "nazwa": "Liceum ogólnokształcące",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.SECONDARY_SCHOOL,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.HIGH_SCHOOL,
    },
    17: {
        "nazwa": "Liceum ogólnokształcące uzupełniające dla absolwentów zasadniczych szkół zawodowych",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.SECONDARY_SCHOOL,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.HIGH_SCHOOL,
    },
    15: {
        "nazwa": "Liceum profilowane",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.SECONDARY_SCHOOL,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.HIGH_SCHOOL,
    },
    27: {
        "nazwa": "Liceum sztuk plastycznych",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.SECONDARY_SCHOOL,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.HIGH_SCHOOL,
    },
    40: {
        "nazwa": "Międzyszkolny ośrodek sportowy",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    38: {
        "nazwa": "Młodzieżowy dom kultury",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    54: {
        "nazwa": "Młodzieżowy Ośrodek Socjoterapii ze szkołami",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    53: {
        "nazwa": "Młodzieżowy Ośrodek Wychowawczy",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    35: {
        "nazwa": "Nauczycielskie Kolegium Języków Obcych",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    75: {
        "nazwa": "Niepubliczna placówka kształcenia ustawicznego i praktycznego",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    83: {
        "nazwa": "Niepubliczna placówka kształcenia ustawicznego i praktycznego ze szkołami",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    64: {
        "nazwa": "Niepubliczna placówka oświatowo-wychowawcza w systemie oświaty",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    39: {
        "nazwa": "Ognisko pracy pozaszkolnej",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    29: {
        "nazwa": "Ogólnokształcąca szkoła baletowa",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    21: {
        "nazwa": "Ogólnokształcąca szkoła muzyczna I stopnia",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    24: {
        "nazwa": "Ogólnokształcąca szkoła muzyczna II stopnia",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    26: {
        "nazwa": "Ogólnokształcąca szkoła sztuk pięknych",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    41: {
        "nazwa": "Ogród jordanowski",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    47: {
        "nazwa": "Ośrodek dokształcania i doskonalenia zawodowego",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    52: {
        "nazwa": "Ośrodek Rewalidacyjno-Wychowawczy",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    37: {
        "nazwa": "Pałac młodzieży",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    57: {
        "nazwa": "Placówka doskonalenia nauczycieli",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    74: {
        "nazwa": "Placówka Kształcenia Ustawicznego - bez szkół",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    46: {
        "nazwa": "Placówka Kształcenia Ustawicznego ze szkołami",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    44: {
        "nazwa": "Placówki artystyczne (ognisko artystyczne)",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    91: {
        "nazwa": "Policealna szkoła muzyczna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    92: {
        "nazwa": "Policealna szkoła plastyczna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    48: {
        "nazwa": "Poradnia psychologiczno-pedagogiczna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    49: {
        "nazwa": "Poradnia specjalistyczna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    42: {
        "nazwa": "Pozaszkolna placówka specjalistyczna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    82: {
        "nazwa": "Poznańska szkoła chóralna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    1: {
        "nazwa": "Przedszkole",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    81: {
        "nazwa": "Punkt przedszkolny",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    51: {
        "nazwa": "Specjalny Ośrodek Szkolno-Wychowawczy",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    50: {
        "nazwa": "Specjalny Ośrodek Wychowawczy",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    43: {
        "nazwa": "Szkolne schronisko młodzieżowe",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    85: {
        "nazwa": "Szkoła muzyczna I stopnia",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    86: {
        "nazwa": "Szkoła muzyczna II stopnia",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    3: {
        "nazwa": "Szkoła podstawowa",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    19: {
        "nazwa": "Szkoła policealna",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    20: {
        "nazwa": "Szkoła specjalna przysposabiająca do pracy",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    31: {
        "nazwa": "Szkoła sztuki cyrkowej",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    87: {
        "nazwa": "Szkoła sztuki tańca",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    16: {
        "nazwa": "Technikum",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.SECONDARY_SCHOOL,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.TECHNICAL_HIGH_SCHOOL,
    },
    100: {
        "nazwa": "Zespół szkół i placówek oświatowych",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
    80: {
        "nazwa": "Zespół wychowania przedszkolnego",
        "level1_generalization": RspoInstitutionTypeLevel1Generalization.OTHER,
        "level2_generalization": RspoInstitutionTypeLevel2Generalization.OTHER,
    },
}
