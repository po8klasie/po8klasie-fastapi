from po8klasie_fastapi.app.lib.testing_utils import (
    TestingFixtures,
    TestClient,
    get_test_db,
)
from po8klasie_fastapi.db.models import RoadAccident

client = TestClient()


def test_returns_422_if_bbox_not_specified():
    response = client.get("/api/search/map_features")

    assert response.status_code == 422


def test_returns_422_if_bbox_invalid():
    response = client.get(
        "/api/search/map_features", params={"bbox": "2.0, 1.0, a, 4.0"}
    )

    assert response.status_code == 422


def test_list_features_contained_by_bbox():
    # given
    TestingFixtures.reset_db()

    db = get_test_db()

    mock_accidents = [
        RoadAccident(sewik_id="1", accident_type_id="1", geometry="POINT(4.0 3.0)"),
        RoadAccident(sewik_id="2", accident_type_id="1", geometry="POINT(5.0 3.0)"),
        RoadAccident(sewik_id="3", accident_type_id="6", geometry="POINT(3.0 3.5)"),
        RoadAccident(sewik_id="4", accident_type_id="3", geometry="POINT(9.0 3.5)"),
    ]
    for acc in mock_accidents:
        db.add(acc)
    db.commit()

    # when

    response = client.get(
        "/api/search/map_features",
        params={"bbox": "2.0,1.0,5.0,4.0"},
    )

    # then

    assert response.status_code == 200
    assert response.json() == {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [4.0, 3.0]},
                "properties": {"sewikId": "1"},
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [3.0, 3.5]},
                "properties": {"sewikId": "3"},
            },
        ],
    }
