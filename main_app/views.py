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
    featured_pets = get_animals()
    return render(request, 'index.html', {
        'animal_types': animal_types,
        'featured_pets': featured_pets
    })


def about(request):
    return render(request, 'about.html')


def search(request):
    if request.method == "POST":
        zip_code = request.POST.get('zip_code', '')
        animal_type = request.POST.get('pet_type', '')
        size = request.POST.get('size', '')
        gender = request.POST.get('gender', '')
        age = request.POST.get('age', '')

        search = {}
        if animal_type:
            search['type'] = animal_type
        if zip_code:
            search['location'] = zip_code
        if size:
            search['size'] = size
        if gender:
            search['gender'] = gender
        if age:
            search['age'] = age
        search['limit'] = 20

        search_string = f'?{urllib.parse.urlencode(search)}'
        return redirect(f'/search/{search_string}')
    else:
        animal_types = get_animal_types()
        featured_pets = get_animals()

        parameters = {
            "animal_types": animal_types,
            "featured_pets": featured_pets
        }

        if request.META['QUERY_STRING'] != '':
            query_str = request.META['QUERY_STRING']
            search_results = filter_animals(f'?{query_str}')
            parameters['search_results'] = search_results

            if 'previous' in search_results['pagination']['_links']:
                parameters['prev_page'] = search_results['pagination']['_links']['previous']['href'][len(
                    '/v2/animals'):]

            if 'next' in search_results['pagination']['_links']:
                parameters['next_page'] = search_results['pagination']['_links']['next']['href'][len(
                    '/v2/animals'):]

        return render(request, 'search.html', parameters)


@login_required
def favorites(request):
    users_pets = request.user.pet_set.all()
    api_pets = []
    for pet in users_pets:
        pet_data = get_animal(pet.api_pet_id)

        if pet_data['animal']['status'] == 'adoptable':
            api_pets.append(pet_data)
        else:
            Pet.objects.filter(api_pet_id=pet.api_pet_id).delete()

    return render(request, 'favorites.html', {'users_pets': api_pets})


def pets_show(request, api_pet_id):
    animal = get_animal(api_pet_id)

    # redirect to favorites if pet id not found
    if 'status' in animal and animal['status'] != 200:
        return redirect('favorites')

    params = {'animal': animal}
    try:
        db_pet = Pet.objects.get(api_pet_id=api_pet_id)
        params['pet'] = db_pet
    except Pet.DoesNotExist:
        pass

    return render(request, 'details.html', params)


@login_required
def pets_update(request):
    api_pet_id = request.POST.get('api_pet_id', '')
    if not api_pet_id:
        return redirect('index')
    current_user = request.user
    comment = request.POST.get('comment', '')
    pet = Pet.objects.get(api_pet_id=api_pet_id, user=current_user)
    pet.comments = comment
    pet.save()
    return redirect('pets_show', api_pet_id)


@login_required
def pets_create(request):
    api_pet_id = request.POST.get('api_pet_id', '')
    if not api_pet_id:
        return redirect('index')
    current_user = request.user
    pet = Pet.objects.create(api_pet_id=api_pet_id, user=current_user)
    pet.save()
    return redirect('pets_show', api_pet_id)


@login_required
def pets_delete(request):
    api_pet_id = request.POST.get('api_pet_id', '')
    if not api_pet_id:
        return redirect('index')
    current_user = request.user
    Pet.objects.filter(api_pet_id=api_pet_id, user=current_user).delete()
    return redirect('favorites')


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
