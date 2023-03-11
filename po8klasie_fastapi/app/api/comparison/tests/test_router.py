from po8klasie_fastapi.app.lib.testing_utils import TestClient

client = TestClient()

COMPARISON_API_PATH = "/api/comparison"


def test_returns_422_if_rspo_list_not_specified():
    response = client.get(COMPARISON_API_PATH)

    assert response.status_code == 422


def test_returns_422_if_more_than_five_rspos_provided():
    response = client.get(
        COMPARISON_API_PATH,
        params={"rspo": ["123", "456", "789", "1011", "1213", "1415"]},
    )

    assert response.status_code == 422


def test_returns_404_if_not_all_rspos_are_found():
    response = client.get(COMPARISON_API_PATH, params={"rspo": ["123"]})

    assert response.status_code == 404
