# Field info
# kod,nazwa,komentarz,opis,ikona,jednostka,okres,ostatnia_aktualizacja
# "w92","Liczba etatów przypadających na jednego nauczyciela"
# "w110","Nauczyciele wspomagający"
# "w161","Uczniowie pochodzący spoza Gdyni"
# "w51","Klasy integracyjne"
# "wx1","Aktualny dzienny koszt oświaty"
# "wx2","Liczba sal lekcyjnych"
# "wx3","Oddziały sportowe"
# "w68","Zmianowość"
# "w88","Liczba uczniów na nauczyciela"
# "opis_szkoły","Opis szkoły"
# "sport", "Zajęcia sportowe oferowane przez szkołę"
# "jezyki_obce", "Zajęcia językowe oferowane przez szkołę"
# "profile_klas", "Profile klas które są oferowane przez daną szkołę"
# "zajecia_dodatkowe", "Zajęcia dodatkowe oferowane przez szkołę"


def add_gdynia_institution_data_to_model(institution_match, institution_data):
    institution_match.classrooms_count = institution_data.get("wx2")
    institution_match.sport_classes_count = institution_data.get("wx3")
    institution_match.working_time = institution_data.get("w68")
    institution_match.students_per_teacher = institution_data.get("w88")
    institution_match.description = institution_data.get("opis_szkoly")
    institution_match.sport_activities = institution_data.get("sport")
    institution_match.foreign_languages = institution_data.get("jezyki_obce")
    institution_match.class_profiles = institution_data.get("profile_klas")
    institution_match.extracurricular_activities = institution_data.get(
        "zajecia_dodatkowe"
    )

    return institution_match
