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


def add_gdynia_facility_data_to_model(facility_match, facility_data):
    facility_match.classrooms_count = facility_data.get("wx2")
    facility_match.sport_classes_count = facility_data.get("wx3")
    facility_match.working_time = facility_data.get("w68")
    facility_match.students_per_teacher = facility_data.get("w88")
    facility_match.description = facility_data.get("opis_szkoly")
    facility_match.sport_activities = facility_data.get("sport")
    facility_match.foreign_languages = facility_data.get("jezyki_obce")
    facility_match.class_profiles = facility_data.get("profile_klas")
    facility_match.extracurricular_activities = facility_data.get("zajecia_dodatkowe")

    return facility_match
