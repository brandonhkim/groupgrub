from dataclasses import dataclass
from .mock_repository import MockRepository

@dataclass
class Business:
    name: str
    categories: list[str]
    price: int
    phone: str

    def __init__(self, name: str, categories: list[str], price: int, phone: str):
        self.name = name
        self.categories = categories
        self.price = price
        self.phone = phone
    
    def __str__(self):
        return (
            "name: " + self.name + '\n' +
            str(self.price) + '\n' + 
            "categories: " + str(self.categories) + '\n' +
            "phone: " + self.phone + '\n'
        )


class MockFusionRepository(MockRepository[Business]):
    def __init__(self):
        burgers = Business(name="burgers", categories=["fast+food", "fried", "meat"], price=2, phone="burgers#")
        fries = Business(name="fries", categories=["fast+food", "fried"], price=2, phone="fries#")
        steaks = Business(name="steaks", categories=["meat"], price=4, phone="steaks#")
        grapes = Business(name="grapes", categories=["fruit"], price=1, phone="grapes#")

        self.businessMap = {
            "fried": [burgers, fries],
            "meat": [burgers, steaks],
            "fruit": [grapes],
            "fast+food": [burgers]
        }


    def get(self, email: str) -> Business:
        raise NotImplementedError
    
    def get_all(self, geolocation: dict, categories: list[str], price: int, num_results: int) -> list[Business]:
        businesses = []
        for category in categories:
            for business in self.businessMap[category]:
                if len(businesses) > num_results: 
                    break
                if business.price <= int(price[-1]):
                    businesses.append(business)
        return businesses
    
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
    
    def update(self, email: str, **kwargs: object) -> None:
        raise NotImplementedError
    
    def delete(self, email: str) -> None:
        raise NotImplementedError
