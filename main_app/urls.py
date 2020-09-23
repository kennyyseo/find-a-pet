from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('favorites/', views.favorites, name='favorites'),
    path('accounts/signup', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('pets/<int:api_pet_id>/', views.pets_show, name='pets'),
    path('pets/create/', views.pets_create, name='pets_create'),
    path('pets/<int:pet_id>/delete/', views.pets_delete, name='pets_delete'),
    path('pets/<int:pet_id>/update/', views.pets_update, name='pets_update'),
]
