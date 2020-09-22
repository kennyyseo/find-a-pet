import os
import requests

# PETFINDER_TOKEN = os.getenv("PETFINDER_TOKEN")
PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")


def get_animals():
    endpoint = 'https://api.petfinder.com/v2/animals'
    return base_request(endpoint)


def get_animal(animal_id):
    endpoint = f'https://api.petfinder.com/v2/animals/{animal_id}'
    return base_request(endpoint)


def get_animal_types():
    endpoint = 'https://api.petfinder.com/v2/types'
    return base_request(endpoint)


def get_animals_type(animal_type):
    endpoint = f'https://api.petfinder.com/v2/types/{animal_type}'
    return base_request(endpoint)


def get_animal_breed(animal_type):
    endpoint = f'https://api.petfinder.com/v2/types/{animal_type}/breeds'
    return base_request(endpoint)


def filter_animals(query_string):
    endpoint = f'https://api.petfinder.com/v2/animals{query_string}'
    return base_request(endpoint)


def base_request(endpoint):
    data = {}
    headers = {'Authorization': 'Bearer ' + get_access_token()}
    response = requests.request('GET', endpoint, headers=headers, data=data)
    return response.json()


def get_access_token():
    endpoint = 'https://api.petfinder.com/v2/oauth2/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': PETFINDER_CLIENT_ID,
        'client_secret': PETFINDER_CLIENT_SECRET
    }
    response = requests.post(endpoint, data=data)
    return response.json()['access_token']
