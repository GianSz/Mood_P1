from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import matplotlib.pyplot as plt
import cv2
from deepface import DeepFace
import numpy as np
import random
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F

# Create your views here.

def register_page(request):
    return render(request, template_name='registro.html')

@login_required(login_url='/login/')
def home_page(request): # Views para la home page
    canciones = Cancion.objects.all()
    contexto = {'canciones':canciones}

    return render(request, template_name='home.html', context=contexto)

@login_required(login_url='/login/')
def miPerfil_page(request): 
    return render(request, template_name='miPerfil.html')

@login_required(login_url='/login/')
def tuMusica_page(request): 
    return render(request, template_name='tuMusica.html')

@login_required(login_url='/login/')
def formsFellings_page(request): 
    return render(request, template_name='formsFellings.html')


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
                #'audio': obj.audio,
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
                    nombre_genr = []
                    nombre_arts = []
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
                        #'audio': obj.audio,
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
                    nombre_genr = []
                    nombre_arts = []
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
                        #'audio': obj.audio,
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

@login_required(login_url='/login/')
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
    canciones=[]
    
    if(userEmotion=="feliz"):
        CancionesAltas=Cancion.objects.filter(frecuencia__in=[4,5]).filter(intensidad_feliz__gte=F('intensidad_enojo')).filter(intensidad_enojo__gte=F('intensidad_triste'))
        #Filtro:
        #frecuencias 4 y 5
        # %Feliz >= %Enojo >= %Triste
        CancionesNeutras=Cancion.objects.filter(frecuencia__in=[3]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 3
        # 20% < %Feliz %Triste Y %Enojo < 45%
        
        while(len(canciones)<4 and CancionesAltas.count()>0):
            cancion = random.choice(CancionesAltas)
            canciones.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(canciones)<5 and CancionesNeutras.count()>0):
            cancion = random.choice(CancionesNeutras)
            canciones.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(canciones)<9 and CancionesAltas.count()>0):
            cancion = random.choice(CancionesAltas)
            canciones.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(canciones)<10 and CancionesNeutras.count()>0):
            cancion = random.choice(CancionesNeutras)
            canciones.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(canciones)<14 and CancionesAltas.count()>0):
            cancion = random.choice(CancionesAltas)
            canciones.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(canciones)<15 and CancionesNeutras.count()>0):
            cancion = random.choice(CancionesNeutras)
            canciones.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)        

    elif(userEmotion=="triste"):
        CancionesEmpatia=Cancion.objects.filter(frecuencia__in=[4,3,2]).filter(intensidad_triste__gte=F('intensidad_feliz')).filter(intensidad_feliz__gte=F('intensidad_enojo'))
        #Filtro:
        #frecuencias 4,3,2
        # %Triste >= %Feliz >= %Enojo
        CancionesMedio=Cancion.objects.filter(frecuencia__in=[3,2]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 3,2
        # 20% < %Feliz %Triste Y %Enojo < 45%
        CancionesSuave=Cancion.objects.filter(frecuencia__in=[2,1]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 2,1
        # 20% < %Feliz %Triste Y %Enojo < 45%

        while(len(canciones)<5 and CancionesEmpatia.count()>0):
            cancion = random.choice(CancionesEmpatia)
            canciones.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)
        
        while(len(canciones)<10 and CancionesMedio.count()>0):
            cancion = random.choice(CancionesMedio)
            canciones.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)

        while(len(canciones)<15 and CancionesSuave.count()>0):
            cancion = random.choice(CancionesSuave)
            canciones.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)
    
    elif(userEmotion=="enojado"):
        CancionesEmpatia=Cancion.objects.filter(frecuencia__in=[5,4,3]).filter(intensidad_enojo__gte=F('intensidad_feliz')).filter(intensidad_feliz__gte=F('intensidad_triste'))
        #Filtro:
        #frecuencias 5,4,3
        # %Enojo >= %Feliz >= %Triste
        CancionesMedio=Cancion.objects.filter(frecuencia__in=[3,2]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 3,2
        # 20% < %Feliz %Triste Y % Enojo < 45%
        CancionesSuave=Cancion.objects.filter(frecuencia__in=[2,1]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 2,1
        # 20% < %Feliz %Triste Y % Enojo < 45%
        
        while(len(canciones)<5 and CancionesEmpatia.count()>0):
            cancion = random.choice(CancionesEmpatia)
            canciones.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)
        
        while(len(canciones)<10 and CancionesMedio.count()>0):
            cancion = random.choice(CancionesMedio)
            canciones.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)

        while(len(canciones)<15 and CancionesSuave.count()>0):
            cancion = random.choice(CancionesSuave)
            canciones.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)

    print(canciones)

    context={'userEmotion':userEmotion,'canciones':canciones}

    return render(request, template_name='playlist.html', context = context)
# @login_required(login_url='/login/')
# def logout_view(request):
#     logout(request)
#     messages.success(request, f'Sesión cerrada correctamente')
#     return login_page(request)