from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import urllib.parse
from .api import *
from .models import Pet

# Create your views here.


def index(request):
    animal_types = get_animal_types()
    return render(request, 'index.html', {'animal_types': animal_types})


def about(request):
    return render(request, 'about.html')


def search(request):

    animal_types = get_animal_types()

    parameters = {
        "animal_types": animal_types
    }

    if request.method == "POST":
        zip_code = request.POST['zip_code']
        animal_type = request.POST['pet_type']

        search = {}

        if animal_type:
            search['type'] = animal_type

        if zip_code:
            search['location'] = zip_code

        search_string = f'?{urllib.parse.urlencode(search)}'
        local_animals = filter_animals(search_string)
        parameters['search_results'] = local_animals

        return render(request, 'search.html', parameters)
    else:
        return render(request, 'search.html', parameters)


@login_required
def favorites(request):
    users_pets = request.user.pet_set.all()
    api_pets = []
    for pet in users_pets:
        pet_data = get_animal(pet.api_pet_id)
        api_pets.append(pet_data)
    return render(request, 'favorites.html', {'users_pets': api_pets})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def details(request, api_pet_id):
    animal = get_animal(api_pet_id)
    db_pet = Pet.objects.get(api_pet_id=api_pet_id)
    return render(request, 'details.html', {'animal': animal, 'pet': db_pet})


def pets_update(request, pet_id):
    comment = request.POST['comment']
    pet = Pet.objects.get(api_pet_id=pet_id)
    pet.comments = comment
    pet.save()
    return redirect('details', pet_id)


def pets_create(request):
    api_pet_id = request.POST['api_pet_id']
    current_user = request.user
    pet = Pet.objects.create(api_pet_id=api_pet_id, user=current_user)
    pet.save()
    return redirect('favorites')


def pets_delete(request, pet_id):
    Pet.objects.filter(api_pet_id=pet_id).delete()
    return redirect('favorites')
