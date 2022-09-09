from urllib import request
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import matplotlib.pyplot as plt
import cv2
from deepface import DeepFace
import numpy as np
from main.models import Sentimiento_Cancion
from django.http import JsonResponse

import requests
import base64

# Create your views here.

def regsiter_page(request):
    auth_object = Spotify_authorization()
    auth_user_token = auth_object.get_auth_user_token()
    auth_url = auth_user_token.url

    return render(request, template_name='registro.html')

def home_page(request): # Views para la home page
    return render(request, template_name='home.html')

# Funcion para el buscador
def get_song(request):
    search = request.GET.get('search')
    payload = []
    nombre_genr = []
    nombre_arts = []

    if search:

        ########### BUSCAR POR TITULO DE LA CANCIÓN ##############################

        objs = Cancion.objects.filter(nombre__startswith=search) #Posible cambio icontains
        
        for obj in objs: # Iterar sobre todas las canciones que empiecen con la busqueda
            genr_songs = Genero_Cancion.objects.filter(id_cancion_id=obj.id) # Obtener las canciones en la tabla genero_cancion en los que el id de la cancion coincida
            #nombre_genr = [] 
            for genr_song in genr_songs: # Iterar sobre todas las relaciones encontradas
                genr = Genero.objects.filter(id=genr_song.id_genero_id) #Obtener los generos que coincidan por el id
                for genres in genr: # Iterar sobre todos los generos obtenidos que coinciden
                    nombre_genr.append(genres.nombre) #Agregar el nombre de los generos al arreglo para desps agregarlos

            arts_songs = Artista_Cancion.objects.filter(id_cancion_id=obj.id)
            #nombre_arts = []
            for arts_song in arts_songs:
                arts = Artista.objects.filter(id=arts_song.id_artista_id)
                for art in arts:
                    nombre_arts.append(art.nombre)

            payload.append({
                'id': obj.id,
                'name': obj.nombre, 
                'audio': obj.audio,
                'img': obj.imagen,
                'length': obj.duracion,
                'frequency': obj.frecuencia,
                'idiom': obj.idioma,
                'genres': nombre_genr,
                'artists': nombre_arts,
            })
        
        nombre_genr = []
        nombre_arts = []

        ########### BUSCAR POR NOMBRE DEL ARTISTA ##############################

        artistas = Artista.objects.filter(nombre__startswith=search)

        for artista in artistas:
            artistas_cancion = Artista_Cancion.objects.filter(id_artista_id=artista.id)
            for artista_cancion in artistas_cancion:
                objs = Cancion.objects.filter(id=artista_cancion.id_cancion_id)
                for obj in objs:
                    genr_songs = Genero_Cancion.objects.filter(id_cancion_id=obj.id) # Obtener las canciones en la tabla genero_cancion en los que el id de la cancion coincida 
                    for genr_song in genr_songs: # Iterar sobre todas las relaciones encontradas
                        genr = Genero.objects.filter(id=genr_song.id_genero_id) #Obtener los generos que coincidan por el id
                        for genres in genr: # Iterar sobre todos los generos obtenidos que coinciden
                            nombre_genr.append(genres.nombre) #Agregar el nombre de los generos al arreglo para desps agregarlos

                    arts_songs = Artista_Cancion.objects.filter(id_cancion_id=obj.id)
                    for arts_song in arts_songs:
                        arts = Artista.objects.filter(id=arts_song.id_artista_id)
                        for art in arts:
                            nombre_arts.append(art.nombre)

                    payload.append({
                        'id': obj.id,
                        'name': obj.nombre, 
                        'audio': obj.audio,
                        'img': obj.imagen,
                        'length': obj.duracion,
                        'frequency': obj.frecuencia,
                        'idiom': obj.idioma,
                        'genres': nombre_genr,
                        'artists': nombre_arts,
                    })
        
        nombre_genr = []
        nombre_arts = []

        ######## BUSCAR POR GENERO ########################

        generos = Genero.objects.filter(nombre__startswith=search)

        for genero in generos:
            generos_cancion = Genero_Cancion.objects.filter(id_genero_id=genero.id)
            for genero_cancion in generos_cancion:
                objs = Cancion.objects.filter(id=genero_cancion.id_cancion_id)
                for obj in objs:
                    genr_songs = Genero_Cancion.objects.filter(id_cancion_id=obj.id) # Obtener las canciones en la tabla genero_cancion en los que el id de la cancion coincida 
                    for genr_song in genr_songs: # Iterar sobre todas las relaciones encontradas
                        genr = Genero.objects.filter(id=genr_song.id_genero_id) #Obtener los generos que coincidan por el id
                        for genres in genr: # Iterar sobre todos los generos obtenidos que coinciden
                            nombre_genr.append(genres.nombre) #Agregar el nombre de los generos al arreglo para desps agregarlos

                    arts_songs = Artista_Cancion.objects.filter(id_cancion_id=obj.id)
                    for arts_song in arts_songs:
                        arts = Artista.objects.filter(id=arts_song.id_artista_id)
                        for art in arts:
                            nombre_arts.append(art.nombre)

                    payload.append({
                        'id': obj.id,
                        'name': obj.nombre, 
                        'audio': obj.audio,
                        'img': obj.imagen,
                        'length': obj.duracion,
                        'frequency': obj.frecuencia,
                        'idiom': obj.idioma,
                        'genres': nombre_genr,
                        'artists': nombre_arts,
                    })
        
        nombre_genr = []
        nombre_arts = []    
                
    return JsonResponse({
        'status': True,
        'payload': payload,
    })

def mood_page(request): #Views para la pagina mood
    return render(request, template_name='mood.html')

def login_page(request): #Views para la pagina mood
    if request.method == 'GET':
        return render(request, template_name='login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Acabas de ingresar como {user.username}')
            return redirect('home')
        else:
            messages.error(request, '¡El usuario y la contraseña no coinciden, por favor vuelva a intentarlo!')
            return redirect('login')
    
    return render(request, template_name='login.html')


def recognize(request): #Views para la pagina mood

    userEmotion = "" #initialize empty variable for storing the users emotion

    video=cv2.VideoCapture(0)  #requisting the input from the webcam or camera

    while video.isOpened():  #verifying if the camera was opened
        _,frame = video.read() #read the camera footage
           
        #we'll do a try and exception to analyze the users emotion
        try:
            #if we can detect a face we use DeepFace.analyze to extract the information (emtion, age, race and) of the user
            analyze = DeepFace.analyze(frame, actions = ['emotion']) 
            userEmotion = analyze['dominant_emotion']  #we only need the users emotion so we take that data

        except:
            userEmotion = " " #if we couldn't detect the users face we store an empty string

        video.release() #stop live footage

        #as this page is in spanish and Deepface is in english we translate the emotions
        if userEmotion == "happy" or userEmotion == "neutral" or userEmotion == "surprised":
            userEmotion = "feliz"

        elif userEmotion == "sad" or userEmotion == "fear":
            userEmotion = "triste"

        elif userEmotion == "angry" or userEmotion == "disgust":
            userEmotion = "enojado"
            
        else: #if the string was empty then the face was not recognized
            userEmotion = "No te hemos reconocido"

    print(userEmotion)

    context={'userEmotion':userEmotion}

    return render(request, template_name='confirmEmotion.html', context=context)

def playlist(request, userEmotion):

    canciones = Sentimiento_Cancion.objects.filter(id_sentimiento__nombre__contains=userEmotion)

    context={'userEmotion':userEmotion,'canciones':canciones}

    return render(request, template_name='playlist.html', context = context)

class Spotify_authorization():
    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    
    CLIENT_ID = "6771adc482d249bab3f377402f1d38c6"
    CLIENT_SECRET = "ed6632a07b87492aad870c0d3b2663e1"
    REDIRECT_URI = "http://localhost:8000/home/"
    scope = "user-modify-playback-state"
    auth_code = ""

    def get_auth_user_token(self):
        auth_user_token = requests.get(self.AUTH_URL, {
            "client_id":self.CLIENT_ID,
            "response_type":"code",
            "scope":self.scope,
            "redirect_uri":self.REDIRECT_URI
        })
        return auth_user_token

    def get_access_token(self):
        token_creds = f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()
        token_creds_b64 = base64.b64encode(token_creds)

        token_data={
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type":"authorization_code",
            "redirect_uri": self.REDIRECT_URI,
            "code": self.auth_code
        }

        token_headers={
            "Authorization": f"Basic {token_creds_b64.decode()}",
            "content-type":"application/x-www-form-urlencoded",
        }

        token_response = requests.post(self.TOKEN_URL, data=token_data, headers=token_headers)

        token_response_json = token_response.json()

        print(token_response_json)

        # access_token = token_response_json["access_token"]
        # refresh_token = token_response_json["refresh_token"]
        # expires_in = token_response_json["expires_in"]
