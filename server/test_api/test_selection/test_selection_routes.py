import json
import pytest
from api.api import create_app
from ..mock_repositories.mock_user_repository import MockUserRepository
from ..mock_repositories.mock_fusion_repository import MockFusionRepository
from ..mock_repositories.mock_preference_repository import MockPreferenceRepository

SAL_ADDRESS = {
    "latitude":   34.02116,
    "longitude": -118.287132
}

TEST_CATEGORIES_ONE = ["fried", "meat"]
TEST_CATEGORIES_TWO = ["fruit"]
TEST_CATEGORIES_THREE = ["fried", "fruit"]
TEST_CATEGORY_SPACE = ["fast food"]

TEST_NUM_RESULTS = 10

def my_client():
    app = create_app(ur=MockUserRepository(), pr=MockPreferenceRepository(), fr=MockFusionRepository())
    app.config.update({
        "TESTING": True,
    })
    return app.test_client()

@pytest.mark.last
class TestSelectionRoutes:
    def test_get_businesses_success(self):
        client = my_client()
        response = client.post("/selection/get-businesses", json={
            "geolocation": SAL_ADDRESS,
            "categories": TEST_CATEGORIES_ONE,
            "num_results": TEST_NUM_RESULTS
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert len(data["selections"]) > 0
        assert status_code == 200

    def test_get_businesses_bad_geolocation(self):
        client = my_client()
        response = client.post("/selection/get-businesses", json={
            "geolocation": {
                "latitude": -180,
                "longitude": -181
            },
            "categories": TEST_CATEGORIES_ONE,
            "num_results": TEST_NUM_RESULTS
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Invalid geolocation coordinates provided"
        assert status_code == 400

    def test_get_businesses_bad_number(self):
        client = my_client()
        for num in [1, 11, 21]:
            response = client.post("/selection/get-businesses", json={
                "geolocation": SAL_ADDRESS,
                "categories": TEST_CATEGORIES_ONE,
                "num_results": num
            })

            data = json.loads(response.get_data(as_text=True))
            status_code = response.status_code

            assert data["status"] == "ERROR"
            assert data["error"] == "Invalid request received"
            assert status_code == 400

    def test_get_businesses_white_space(self):
        client = my_client()
        response = client.post("/selection/get-businesses", json={
            "geolocation": SAL_ADDRESS,
            "categories": TEST_CATEGORY_SPACE,
            "num_results": TEST_NUM_RESULTS
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert len(data["selections"]) > 0
        assert status_code == 200
        
    def test_get_businesses_no_matches(self):
        client = my_client()
        response = client.post("/selection/get-businesses", json={
            "geolocation": SAL_ADDRESS,
            "categories": [],
            "num_results": TEST_NUM_RESULTS
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "No results available"
        assert status_code == 400

