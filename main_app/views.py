from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .api import *
from .models import Pet

# Create your views here.


def index(request):
    return render(request, 'index.html', )


def about(request):
    return render(request, 'about.html')


def search(request):
    zip_code = request.GET['zip_code']
    local_animals = filter_animals(f"?location={zip_code}")
    return render(request, 'search.html', {"local_animals": local_animals})


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
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def details(request, api_pet_id):
    animal = get_animal(api_pet_id)
    return render(request, 'details.html', {'animal': animal})


def pets_create(request):
    api_pet_id = request.POST['api_pet_id']
    current_user = request.user
    pet = Pet.objects.create(api_pet_id=api_pet_id, user=current_user)
    pet.save()
    return redirect('favorites')


def pets_delete(request, pet_id):
    # delete row in db with pet id that's in the request
    # redirect back to favorites
    Pet.objects.filter(api_pet_id=pet_id).delete()
    return redirect('favorites')
