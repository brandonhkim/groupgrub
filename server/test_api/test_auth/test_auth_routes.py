import json
import pytest
from api.api import create_app
from ..mock_repositories.mock_user_repository import MockUserRepository
from ..mock_repositories.mock_fusion_repository import MockFusionRepository

TEST_EMAIL_ONE = 'one@email.com'
TEST_PASSWORD_ONE = 'abc123'
TEST_PREFERENCES_ONE = {
    "New" : {
        "name": "New",
        "code" : "New_code"
    },
    "Test" : {
        "name": "Test",
        "code" : "Test_code"
    },
    "Preferences" : {
        "name": "Preferences",
        "code" : "Preferences_code"
    },
}


TEST_EMAIL_TWO = 'two@email.com'
TEST_PASSWORD_TWO = 'cba321'
TEST_PREFERENCES_TWO = {
    "Second" : {
        "name": "Second",
        "code" : "Second_code"
    },
    "2nd" : {
        "name": "2nd",
        "code" : "2nd_code"
    },
}

@pytest.fixture()
def my_app():
    app = create_app(ur=MockUserRepository(), fr=MockFusionRepository())
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def my_client(my_app):
    return my_app.test_client()

class TestAuthRoutes():
    def test_register_success(self, my_client):
        response = my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        })

        data = json.loads(response.get_data(as_text=True))
        id = data["id"]
        status_code = response.status_code

        assert int(id, 16) and id.islower()
        assert status_code == 200

    def test_register_fail(self, my_client):
        my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        })

        response = my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Email already exists"
        assert status_code == 409

    def test_me_success(self, my_client):
        # Register a test user
        user = json.loads(my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        }).get_data(as_text=True))

        # Test /auth/@me route
        response = my_client.get("/auth/@me")

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["id"] == user["id"]
        assert data["email"] == user["email"]
        assert status_code == 200
        
    def test_me_fail(self, my_client):
        response = my_client.get("/auth/@me")

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Invalid session token"
        assert status_code == 401

    def test_logout_without_session(self, my_client):
        response = my_client.post("/auth/logout")

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "SUCCESS"
        assert status_code == 200

    def test_logout_with_session(self, my_client):
        # Register user
        my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        })
        
        # Attempt logout
        response = my_client.post("/auth/logout")

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "SUCCESS"
        assert status_code == 200

    def test_login_bad_user(self, my_client):
        response = my_client.post("/auth/login", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Unauthorized"
        assert status_code == 401

    def test_login_bad_password(self, my_client):
        # Register user and logout
        my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        })
        my_client.post("/auth/logout")

        # Begin login attempt
        response = my_client.post("/auth/login", json={
            "email": TEST_EMAIL_ONE,
            "password": "incorrect_password"
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Unauthorized"
        assert status_code == 401

    def test_login_success(self, my_client):
        # Register user and logout
        user = json.loads(my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        }).get_data(as_text=True))
        my_client.post("/auth/logout")

        # Begin login attempt
        response = my_client.post("/auth/login", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["id"] == user["id"]
        assert data["email"] == TEST_EMAIL_ONE
        assert status_code == 200

    def test_update_password_no_session(self, my_client):
        response = my_client.post("/auth/update-password", json={
                    "email": TEST_EMAIL_ONE,
                    "password": TEST_PASSWORD_ONE
                })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Invalid session token"
        assert status_code == 401

    def test_update_password_success(self, my_client):
        # Register user (also acts as login)
        user = json.loads(my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        }).get_data(as_text=True))

        # Update Password
        response = my_client.post("/auth/update-password", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_TWO
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["id"] == user["id"]
        assert data["email"] == TEST_EMAIL_ONE
        assert status_code == 200

        # Logout user
        my_client.post("/auth/logout")

        # Login with new password
        response = my_client.post("/auth/login", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_TWO
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["id"] == user["id"]
        assert data["email"] == TEST_EMAIL_ONE
        assert status_code == 200

    def test_update_preferences_no_session(self, my_client):
        response = my_client.post("/auth/update-preferences", json={
            "email": TEST_EMAIL_ONE,
            "preferences": TEST_PREFERENCES_ONE
        })

        # Attempt to update preferences
        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Invalid session token"
        assert status_code == 401

    def test_update_preferences_success(self, my_client):
        # Register user (also acts as login)
        user = json.loads(my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        }).get_data(as_text=True))

        # Attempt to update preferences
        response = my_client.post("/auth/update-preferences", json={
            "email": TEST_EMAIL_ONE,
            "preferences": TEST_PREFERENCES_TWO
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["id"] == user["id"]
        assert data["email"] == TEST_EMAIL_ONE
        assert data["preferences"] == TEST_PREFERENCES_ONE | TEST_PREFERENCES_TWO
        assert status_code == 200

    def test_update_preferences_persist(self, my_client):
        # Register user (also acts as login)
        user = json.loads(my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        }).get_data(as_text=True))

        # Update preferences the first time
        response = my_client.post("/auth/update-preferences", json={
            "email": TEST_EMAIL_ONE,
            "preferences": TEST_PREFERENCES_TWO
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["id"] == user["id"]
        assert data["email"] == TEST_EMAIL_ONE
        assert data["preferences"] == TEST_PREFERENCES_ONE | TEST_PREFERENCES_TWO
        assert status_code == 200

        # Update preferences a second time
        response = my_client.post("/auth/update-preferences", json={
            "email": TEST_EMAIL_ONE,
            "preferences": TEST_PREFERENCES_TWO
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["id"] == user["id"]
        assert data["email"] == TEST_EMAIL_ONE
        assert data["preferences"] == TEST_PREFERENCES_ONE | TEST_PREFERENCES_TWO
        assert status_code == 200

    def test_get_preferences_no_session(self, my_client):
        response = my_client.get("/auth/get-preferences")

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Invalid session token"
        assert status_code == 401

    def test_get_preferences_success(self, my_client):
        # Register user (also acts as login)
        user = json.loads(my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        }).get_data(as_text=True))

        # Update preferences
        response = my_client.post("/auth/update-preferences", json={
            "email": TEST_EMAIL_ONE,
            "preferences": TEST_PREFERENCES_ONE
        })

        # Attempt to get preferences
        response = my_client.get("/auth/get-preferences")

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["id"] == user["id"]
        assert data["email"] == TEST_EMAIL_ONE
        assert data["preferences"] == TEST_PREFERENCES_ONE
        assert status_code == 200

    def test_delete_no_session(self, my_client):
        response = my_client.post("/auth/delete", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Invalid session token"
        assert status_code == 401
    
    def test_delete_success(self, my_client):
        # Register user (also acts as login + user/preference instantiation)
        user = json.loads(my_client.post("/auth/register", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
            "preferences": TEST_PREFERENCES_ONE
        }).get_data(as_text=True))

        response = my_client.post("/auth/delete", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "SUCCESS"
        assert status_code == 200

        # Attempt to login - should not be possible
        response = my_client.post("/auth/login", json={
            "email": TEST_EMAIL_ONE,
            "password": TEST_PASSWORD_ONE,
        })

        data = json.loads(response.get_data(as_text=True))
        status_code = response.status_code

        assert data["status"] == "ERROR"
        assert data["error"] == "Unauthorized"
        assert status_code == 401
