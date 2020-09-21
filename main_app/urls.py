from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('favorites/', views.favorites, name='favorites'),
    path('accounts/signup', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('details/<int:api_pet_id>/', views.details, name='details'),
    path('pets/create/', views.pets_create, name='pets_create'),
    path('pets/<int:pet_id>/delete/',
         views.pets_delete, name='pets_delete'),
]
