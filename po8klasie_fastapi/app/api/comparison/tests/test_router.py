from po8klasie_fastapi.app.lib.testing_utils import ClientTestCase

COMPARISON_API_PATH = "/api/comparison"


class ErrorsTestCase(ClientTestCase):
    def test_returns_422_if_rspo_list_not_specified(self):
        response = self.client.get(COMPARISON_API_PATH)

        self.assertEqual(response.status_code, 422)

    def test_returns_422_if_more_than_five_rspos_provided(self):
        response = self.client.get(
            COMPARISON_API_PATH,
            params={"rspo": ["123", "456", "789", "1011", "1213", "1415"]},
        )

        self.assertEqual(response.status_code, 422)

    def test_returns_404_if_not_all_rspos_are_found(self):
        response = self.client.get(COMPARISON_API_PATH, params={"rspo": ["123"]})

        self.assertEqual(response.status_code, 404)
