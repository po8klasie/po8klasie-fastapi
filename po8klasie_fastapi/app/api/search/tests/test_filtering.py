from po8klasie_fastapi.app.api.search.filtering import (
    filter_by_extended_subjects,
    filter_by_languages,
    filter_by_points_threshold,
    filter_by_project_id,
    filter_by_query,
)
from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution
from po8klasie_fastapi.app.institution.tests.factories import (
    SecondarySchoolInstitutionFactory,
)
from po8klasie_fastapi.app.institution_classes.tests.factories import (
    SecondarySchoolInstitutionClassFactory,
)
from po8klasie_fastapi.app.lib.testing_utils import DatabaseTestCase
from po8klasie_fastapi.app.project.tests.factories import ProjectFactory
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution


class SingleFilterTestCase(DatabaseTestCase):
    def _query_db(self):
        return self.session.query(SecondarySchoolInstitution).join(RspoInstitution)

    def assertRspos(self, filtered_results, rspos):
        return self.assertCountEqual([inst.rspo for inst in filtered_results], rspos)


class QueryFilterTestCase(SingleFilterTestCase):
    def _get_filtered_results(self, query):
        return filter_by_query(self._query_db(), query).all()

    def test_contains(self):
        SecondarySchoolInstitutionFactory(rspo_institution__name="Institution #1")
        SecondarySchoolInstitutionFactory(rspo_institution__name="Institution #2")

        filtered_results = self._get_filtered_results("#2")

        self.assertEqual(len(filtered_results), 1)
        self.assertEqual(filtered_results[0].rspo_institution.name, "Institution #2")

    def test_case_insensitive(self):
        SecondarySchoolInstitutionFactory(rspo_institution__name="foo")
        filtered_results = self._get_filtered_results("FOO")

        self.assertEqual(len(filtered_results), 1)
        self.assertEqual(filtered_results[0].rspo_institution.name, "foo")


class ProjectIdFilterTestCase(SingleFilterTestCase):
    def _get_filtered_results(self, project_id):
        return filter_by_project_id(self._query_db(), project_id).all()

    def test_match_project_id(self):
        ProjectFactory(project_name="new_york")
        ProjectFactory(project_name="london")

        SecondarySchoolInstitutionFactory(project_id="new_york")
        SecondarySchoolInstitutionFactory(project_id="london")

        filtered_results = self._get_filtered_results("london")

        self.assertEqual(len(filtered_results), 1)
        self.assertEqual(filtered_results[0].project_id, "london")

    def test_doesnt_match_non_exact_project_id(self):
        ProjectFactory(project_name="new_york")

        SecondarySchoolInstitutionFactory(project_id="new_york")
        filtered_results = self._get_filtered_results("new")

        self.assertEqual(len(filtered_results), 0)


class LanguagesFilterTestCase(SingleFilterTestCase):
    def _get_filtered_results(self, languages):
        return filter_by_languages(self._query_db(), languages).all()

    def test_match_by_many_languages(self):
        SecondarySchoolInstitutionFactory(available_languages=["english", "spanish"])
        SecondarySchoolInstitutionFactory(
            available_languages=["german", "french", "dutch"]
        )

        filtered_results = self._get_filtered_results(["german", "french"])

        self.assertEqual(len(filtered_results), 1)
        self.assertCountEqual(
            filtered_results[0].available_languages, ["german", "french", "dutch"]
        )

    def test_filter_is_school_exclusive(self):
        SecondarySchoolInstitutionFactory(available_languages=["english", "spanish"])
        SecondarySchoolInstitutionFactory(
            available_languages=["german", "french", "dutch"]
        )

        filtered_results = self._get_filtered_results(["english", "german"])

        self.assertEqual(len(filtered_results), 0)


class PointsThresholdFilterTestCase(SingleFilterTestCase):
    def _get_filtered_results(self, threshold):
        return filter_by_points_threshold(self._query_db(), threshold).all()

    def test_dont_filter_if_input_arr_len_invalid(self):
        SecondarySchoolInstitutionFactory(points_stats_min=150, points_stats_max=170)
        SecondarySchoolInstitutionFactory(points_stats_min=100, points_stats_max=110)

        filtered_results = self._get_filtered_results([100])
        self.assertEqual(len(filtered_results), 2)

        filtered_results = self._get_filtered_results([0, 100, 200])
        self.assertEqual(len(filtered_results), 2)

    def test_dont_filter_if_threshold_invalid(self):
        SecondarySchoolInstitutionFactory(points_stats_min=150, points_stats_max=170)
        SecondarySchoolInstitutionFactory(points_stats_min=100, points_stats_max=110)

        filtered_results = self._get_filtered_results([-1, 50])
        self.assertEqual(len(filtered_results), 2)

        filtered_results = self._get_filtered_results([180, 230])
        self.assertEqual(len(filtered_results), 2)

    def test_filter_within_range(self):
        SecondarySchoolInstitutionFactory(
            rspo="bar", points_stats_min=150, points_stats_max=170
        )
        SecondarySchoolInstitutionFactory(
            rspo="foo", points_stats_min=100, points_stats_max=120
        )

        filtered_results = self._get_filtered_results([105, 115])

        self.assertRspos(filtered_results, ["foo"])

    def test_filter_outside_range(self):
        SecondarySchoolInstitutionFactory(
            rspo="bar", points_stats_min=150, points_stats_max=170
        )
        SecondarySchoolInstitutionFactory(
            rspo="foo", points_stats_min=100, points_stats_max=110
        )

        filtered_results = self._get_filtered_results([100, 120])

        self.assertRspos(filtered_results, ["foo"])

    def test_filter_range_reversed(self):
        SecondarySchoolInstitutionFactory(
            rspo="bar", points_stats_min=150, points_stats_max=170
        )
        SecondarySchoolInstitutionFactory(
            rspo="foo", points_stats_min=100, points_stats_max=110
        )

        filtered_results = self._get_filtered_results([120, 100])

        self.assertRspos(filtered_results, ["foo"])


class ExtendedSubjectsFilterTestCase(SingleFilterTestCase):
    def _get_filtered_results(self, extended_subjects):
        return filter_by_extended_subjects(self._query_db(), extended_subjects).all()

    def _create_secondary_schools_by_rspos(self, rspos):
        for rspo in rspos:
            SecondarySchoolInstitutionFactory(rspo=rspo)

    def test_filter_single_value(self):
        self._create_secondary_schools_by_rspos(["foo", "bar"])

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["english", "math"], year=2023, institution_rspo="foo"
        )

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["polish", "art"], year=2023, institution_rspo="bar"
        )

        filtered_results = self._get_filtered_results([["english"]])

        self.assertRspos(filtered_results, ["foo"])

    def test_filter_exclusive_subjects_per_class(self):
        self._create_secondary_schools_by_rspos(["foo", "bar", "fizz"])

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["english", "math"], year=2023, institution_rspo="foo"
        )

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["polish", "art"], year=2023, institution_rspo="bar"
        )

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["french", "history"], year=2023, institution_rspo="fizz"
        )

        filtered_results = self._get_filtered_results([["english", "art", "history"]])

        self.assertEqual(len(filtered_results), 0)

    def test_filter_single_class(self):
        self._create_secondary_schools_by_rspos(["foo", "bar", "fizz"])

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["english", "math"], year=2023, institution_rspo="foo"
        )

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["polish", "art"], year=2023, institution_rspo="bar"
        )

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["french", "history"], year=2023, institution_rspo="fizz"
        )

        filtered_results = self._get_filtered_results([["english"], ["polish"]])

        self.assertRspos(filtered_results, ["foo", "bar"])

    def test_filter_current_class(self):
        self._create_secondary_schools_by_rspos(["foo", "bar", "fizz"])

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["polish", "math"], year=2020, institution_rspo="foo"
        )

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["polish", "art"], year=2023, institution_rspo="bar"
        )

        SecondarySchoolInstitutionClassFactory(
            extended_subjects=["polish", "history"], year=2023, institution_rspo="fizz"
        )

        filtered_results = self._get_filtered_results([["polish"]])

        self.assertRspos(filtered_results, ["bar", "fizz"])
