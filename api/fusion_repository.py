import os
import json
import requests
from Classes.Business import Business

# TODO: ensure that 'search?term=' suffix is correct
ENDPOINT = 'https://api.yelp.com/v3/businesses/search?term='

class FusionRepository:
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {os.environ.get("FUSION_KEY")}',
            'accept': 'application/json',
        }

    '''
        TODO:
          - catch invalid geolocation
          - set default categories if unprovided
          - create react component w/ number of results
          - catch any errors from the query
    '''
    def getRestaurants(self, geolocation: list[str], categories: list[str], num_results: int) -> list[Business]:
        latitude, longitude = geolocation

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



    # TODO: code below will be moved to its own, separate test file
    def test(self):
        latitude = '33.866669'
        longitude = '-117.566666'
        url = ENDPOINT + '/businesses/search?term=mcdonalds' + f'&latitude={latitude}&longitude={longitude}&limit=3&offset=0'

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
            
        return businesses




        