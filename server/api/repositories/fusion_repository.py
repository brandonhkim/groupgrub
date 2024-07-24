import requests
from dataclasses import dataclass
from .repository import Repository
from .templates.fusion_header import fusion_header

# TODO: ensure that 'search?term=' suffix is correct    
ENDPOINT = 'https://api.yelp.com/v3/businesses/search?term=food&categories='

@dataclass
class Business:
    name: str
    categories: list[str]
    url: str
    image_url: str
    price: int
    address: str
    phone: str

    def __init__(self, name: str, categories: list[str], url: str, image_url: str, price: int, address: str, phone: str):
        self.name = name
        self.categories = categories
        self.url = url
        self.image_url =image_url
        self.price = price
        self.address = address
        self.phone = phone
    
    def __str__(self):
        return (
            "name: " + self.name + '\n' +
            str(self.price) + '\n' + 
            "categories: " + str(self.categories) + '\n' +
            "address:" +  self.address + '\n' +
            "phone: " + self.phone + '\n' +
            "url: " + self.url
        )


class FusionRepository(Repository[Business]):
    def __init__(self):
        self.headers = fusion_header
    
    def add(self, **kwargs: object) -> None:
        return NotImplementedError

    def get(self, email: str) -> Business:
        return NotImplementedError
    
    def get_all(self, geolocation: dict, categories: list[str], price: int, num_results: int, radius: int) -> list[Business]:
        latitude, longitude = geolocation['latitude'], geolocation['longitude']

        # build the query url
        formatted_cats = '&categories='.join(categories)
        formatted_price = f'&price={price}'
        formatted_location = f'&latitude={latitude}&longitude={longitude}'
        formatted_radius = f'&radius={radius}'
        formatted_limiter = f'&sort_by=best_match&limit={num_results}'
        formatted_url = ENDPOINT + formatted_cats + formatted_price + formatted_location + formatted_radius + formatted_limiter
        # catch exceptions
        try:
            r = requests.get(formatted_url, headers=self.headers)
        except requests.exceptions.RequestException as e:
            print(e)
            return []

        # extract businesses from json object, and convert objects into Business class
        r = r.json()['businesses']
        businesses = []
        for obj in r:
            # Join list of address lines to a singular string
            address = obj['location']['display_address']
            formatted_address = 'Address not provided'
            if (address and all(isinstance(ele, str) for ele in address)):
                formatted_address = '\n'.join(address)
            data = {
                'name': obj['name'],
                'categories': obj['categories'], 
                'url': obj['url'],
                'image_url': obj['image_url'],
                'price': obj['price'], 
                'address': formatted_address,
                'phone': obj['phone'], 
            }  
            businesses.append(Business(**data))
        
        return businesses
    
    def update(self, email: str, **kwargs: object) -> None:
        return NotImplementedError
    
    def delete(self, email: str) -> None:
        return NotImplementedError

