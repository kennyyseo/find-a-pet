from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('favorites/', views.favorites, name='favorites'),
    path('accounts/signup', views.signup, name='signup'),
    path('search/', views.search, name='search'),
]
