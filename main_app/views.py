from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse('Welcome to Find-a-Pet')


def about(request):
    return render(request, 'about.html')


def home_index(request):
    return render(request, 'home/index.html', )
