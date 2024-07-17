import json
from api.api import create_app
from ..mock_repositories.mock_user_repository import MockUserRepository
from ..mock_repositories.mock_fusion_repository import MockFusionRepository

SAL_ADDRESS = {
    "latitude":   34.02116,
    "longitude": -118.287132
}

TEST_CATEGORIES = ["fried", "meat"]
TEST_CATEGORIES_SPACE = ["fast food"]
TEST_PRICE = 4
TEST_NUM_RESULTS = 10

def my_client():
    app = create_app(ur=MockUserRepository(), fr=MockFusionRepository())
    app.config.update({
        "TESTING": True,
    })
    return app.test_client()

class TestSelectionRoutes:
    def test_get_businesses_success(self):
        client = my_client()
        response = client.post("/selection/get-businesses", json={
            "geolocation": SAL_ADDRESS,
            "categories": TEST_CATEGORIES,
            "price": TEST_PRICE,
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
            "categories": TEST_CATEGORIES,
            "price": TEST_PRICE,
            "num_results": TEST_NUM_RESULTS
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Invalid geolocation coordinates provided"
        assert status_code == 400

    def test_get_businesses_bad_price(self):
        client = my_client()
        for num in [1, 11, 21]:
            response = client.post("/selection/get-businesses", json={
                "geolocation": SAL_ADDRESS,
                "categories": TEST_CATEGORIES,
                "price": 5,
                "num_results": TEST_NUM_RESULTS
            })

            data = json.loads(response.get_data(as_text=True))
            status_code = response.status_code

            assert data["status"] == "ERROR"
            assert data["error"] == "Invalid price range requested"
            assert status_code == 400

    def test_get_businesses_bad_number(self):
        client = my_client()
        for num in [1, 11, 21]:
            response = client.post("/selection/get-businesses", json={
                "geolocation": SAL_ADDRESS,
                "categories": TEST_CATEGORIES,
            "price": TEST_PRICE,
                "num_results": num
            })

            data = json.loads(response.get_data(as_text=True))
            status_code = response.status_code

            assert data["status"] == "ERROR"
            assert data["error"] == "Invalid number of results requested"
            assert status_code == 400

    def test_get_businesses_white_space(self):
        client = my_client()
        response = client.post("/selection/get-businesses", json={
            "geolocation": SAL_ADDRESS,
            "categories": TEST_CATEGORIES_SPACE,
            "price": TEST_PRICE,
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
            "price": TEST_PRICE,
            "num_results": TEST_NUM_RESULTS
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "No results available"
        assert status_code == 400

