from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .api import *
from main_app.forms import HomeSearchForm
from django.views.generic.edit import FormView

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
    return render(request, 'favorites.html')


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


# class HomeSearchView(FormView):
#     template_name = 'index.html'
#     form_class = HomeSearchForm
#     success_url = '/search/'
