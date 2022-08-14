from django.urls import path # Como este es un archivo creado por mi, yo mismo pongo la importación
from main import views

urlpatterns = [
    path('', views.home_page, name='home'), # Esta se debe cambiar a que dirija al login de primerazo
    path('home/', views.home_page, name='home'),
    path('mood/', views.moood_page, name='mood'),
]