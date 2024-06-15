import requests
from dataclasses import dataclass
from .repository import Repository
from .templates.fusion_header import fusion_header

# TODO: ensure that 'search?term=' suffix is correct
ENDPOINT = 'https://api.yelp.com/v3/businesses/search?term='

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


class FusionRepository(Repository[Business]):
    def __init__(self):
        self.headers = fusion_header
    
    def add(self, **kwargs: object) -> None:
        return NotImplementedError

    def get(self, email: str) -> Business:
        return NotImplementedError
    
    def get_all(self, geolocation: dict, categories: list[str], num_results: int) -> list[Business]:
        latitude, longitude = geolocation['latitude'], geolocation['longitude']

        # build the query url
        formatted_cats = '&'.join(categories)
        formatted_location = f'&latitude={latitude}&longitude={longitude}'
        formatted_limiter = f'&limit={num_results}&offset=0'
        formatted_url = ENDPOINT + formatted_cats + formatted_location + formatted_limiter


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
            data = {
                'name': obj['name'],
                'categories': obj['categories'], 
                'rating': obj['rating'], 
                'phone': obj['phone'], 
            }  
            businesses.append(Business(**data))
        
        return businesses
    
    def update(self, email: str, **kwargs: object) -> None:
        return NotImplementedError
    
    def delete(self, email: str) -> None:
        return NotImplementedError

    # TODO: code below will be moved to its own, separate test file
    def test(self):
        latitude = '33.866669'
        longitude = '-117.566666'
        url = ENDPOINT + 'mcdonalds' + f'&latitude={latitude}&longitude={longitude}&limit=3&offset=0'

        r = requests.get(url, headers=self.headers).json()['businesses']
        businesses = []
        
        for business in r:
            significant = {
                'rating': business['rating'], 
                'phone': business['phone'], 
                'categories': business['categories'], 
                'name': business['name']
            }
            businesses.append(Business(**significant))
            
        print(url)
        return businesses




        