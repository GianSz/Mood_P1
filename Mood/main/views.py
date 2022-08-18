from urllib import request
from django.shortcuts import render

# Create your views here.

def home_page(request): # Views para la home page
    return render(request, template_name='home.html')

def mood_page(request): #Views para la pagina mood
    return render(request, template_name='mood.html')