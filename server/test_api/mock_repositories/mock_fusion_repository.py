from dataclasses import dataclass
from .mock_repository import MockRepository

@dataclass
class Business:
    name: str
    categories: list[str]
    rating: float
    phone: str

    def __init__(self, name: str, categories: list[str], rating: float, phone: str):
        self.name = name
        self.categories = categories
        self.rating = rating
        self.phone = phone
    
    def __str__(self):
        return (
            "name: " + self.name + '\n' +
            str(self.rating) + " stars" + '\n' + 
            "categories: " + str(self.categories) + '\n' +
            "phone: " + self.phone + '\n'
        )


class MockFusionRepository(MockRepository[Business]):
    def __init__(self):
        burgers = Business(name="burgers", categories=["fast+food", "fried", "meat"], rating=5.0, phone="burgers#")
        fries = Business(name="fries", categories=["fast+food", "fried"], rating=3.0, phone="fries#")
        steaks = Business(name="steaks", categories=["meat"], rating=1.0, phone="steaks#")
        grapes = Business(name="grapes", categories=["fruit"], rating=4.0, phone="grapes#")

        self.businesses = {
            "fried": [burgers, fries],
            "meat": [burgers, steaks],
            "fruit": [grapes],
            "fast+food": [burgers]
        }

    def get(self, email: str) -> Business:
        raise NotImplementedError
    
    def get_all(self, geolocation: dict, categories: list[str], num_results: int) -> list[Business]:
        businesses = []
        for category in categories:
            if category in self.businesses:
                businesses.extend(self.businesses[category])
        return businesses
    
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
    
    def update(self, email: str, **kwargs: object) -> None:
        raise NotImplementedError
    
    def delete(self, email: str) -> None:
        raise NotImplementedError
