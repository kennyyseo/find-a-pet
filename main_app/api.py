import os
import requests

PETFINDER_TOKEN = os.getenv("PETFINDER_TOKEN")
PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")


def get_animals():
    endpoint = 'https://api.petfinder.com/v2/animals'
    data = {}
    headers = {'Authorization': 'Bearer ' + PETFINDER_TOKEN}
    response = requests.request('get', endpoint, headers=headers, data=data)
    return response.json()


def get_animal(animal_id):
    endpoint = f'https://api.petfinder.com/v2/animals/{animal_id}'
    data = {}
    headers = {'Authorization': 'Bearer ' + PETFINDER_TOKEN}
    response = requests.request('get', endpoint, headers=headers, data=data)
    return response.json()


def get_animal_types():
    endpoint = 'https://api.petfinder.com/v2/types'
    data = {}
    print(PETFINDER_TOKEN)
    headers = {'Authorization': 'Bearer ' + PETFINDER_TOKEN}
    response = requests.request('get', endpoint, headers=headers, data=data)
    return response.json()


def get_animals_type(animal_type):
    endpoint = f'https://api.petfinder.com/v2/types/{animal_type}'
    data = {}
    headers = {'Authorization': 'Bearer ' + PETFINDER_TOKEN}
    response = requests.request('get', endpoint, headers=headers, data=data)
    return response.json()


def get_animal_breed(animal_type):
    endpoint = f'https://api.petfinder.com/v2/types/{animal_type}/breeds'
    data = {}
    headers = {'Authorization': 'Bearer ' + PETFINDER_TOKEN}
    response = requests.request('get', endpoint, headers=headers, data=data)
    return response.json()


def filter_animals(query_string):
    endpoint = f'https://api.petfinder.com/v2/animals{query_string}'
    data = {}
    headers = {'Authorization': 'Bearer ' + PETFINDER_TOKEN}
    response = requests.request('get', endpoint, headers=headers, data=data)
    return response.json()
