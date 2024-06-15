import pytest
from api.repositories.templates.fusion_header import fusion_header
from api.repositories.fusion_repository import Business, FusionRepository

TEST_NAME = "McDonald's"
TEST_CATEGORIES = ['Burger', 'Fast+Food']
TEST_RATING = 3.2
TEST_PHONE = "xxx-xxx-xxxx"

@pytest.fixture
def my_business() -> Business:
    return Business(name=TEST_NAME, categories=TEST_CATEGORIES, rating=TEST_RATING, phone=TEST_PHONE)

@pytest.fixture
def sal_geolocation() -> dict:
    return {
        'latitude': '33.866669',
        'longitude': '-117.566666'
    }

@pytest.fixture
def my_repository() -> FusionRepository:
    return FusionRepository()

class TestBusiness:
    def test_init(self, my_business):
        assert my_business.name == TEST_NAME
        assert my_business.categories == TEST_CATEGORIES
        assert my_business.rating == TEST_RATING
        assert my_business.phone == TEST_PHONE
    

class TestFusionRepository:
    def test_init_repository(self, my_repository):
        assert my_repository.headers == fusion_header

    def test_add(self, my_business, my_repository):
        assert my_repository.add(**vars(my_business)) == NotImplementedError

    def test_get(self, my_repository):
        assert my_repository.get(email="") == NotImplementedError

    def test_get_all_single_result(self, my_business, sal_geolocation, my_repository):
        response = my_repository.get_all(geolocation=sal_geolocation, categories=my_business.categories, num_results = 1)
        assert len(response) == 1
        
        matched_flag = False
        for category in response[0].categories:
            alias, title = category['alias'], category['title']
            for category in my_business.categories:
                if alias in category or category in alias or title in category or category in title:
                    matched_flag = True
        assert matched_flag
    
    def test_get_all_multiple_results(self, my_business, sal_geolocation, my_repository):
        response = my_repository.get_all(geolocation=sal_geolocation, categories=my_business.categories, num_results = 3)
        assert len(response) == 3
        
        matched_flag = True
        for i in range(3):
            cur_match = False
            for category in response[0].categories:
                alias, title = category['alias'], category['title']
                for category in my_business.categories:
                    if alias in category or category in alias or title in category or category in title:
                        cur_match = True
                    if cur_match:
                        break
            if not cur_match:
                matched_flag = False
                break
        
        # If reached, then ALL of the received businesses had at least one matching category
        assert matched_flag
    
    def test_update(self, my_business, my_repository):
        assert my_repository.update(email="", **vars(my_business)) == NotImplementedError
    
    def test_delete(self, my_repository):
        assert my_repository.delete(email="") == NotImplementedError
