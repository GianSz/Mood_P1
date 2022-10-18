from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from matplotlib.style import context
from .models import *
import matplotlib.pyplot as plt
import cv2
from deepface import DeepFace
import numpy as np
import random
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
import csv;
import json;
from datetime import datetime, date
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

# Create your views here.

def handle_not_found(request,exception):
    return render(request,template_name='error404.html')

def register_page(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            fecha = datetime.strptime(request.POST["birthDate"], '%Y-%m-%d')
            hoy = date.today()
            edad = hoy.year - fecha.year
            if(edad >= 15):
                form.save()
                usuarioActual = User.objects.get(username= request.POST["username"])
                nuevoPerfil = Perfil(usuario = usuarioActual, fecha_nacimiento = fecha)
                nuevoPerfil.save()
                login(request, usuarioActual)
                return redirect('formsFellings')
            else:
                return render(request, template_name='registro.html', context = {'form': form, 'error': "Debes tener más de 15 años"})

    return render(request, template_name='registro.html', context = {'form': form, 'error': "None"})

@login_required(login_url='/login/')
def home_page(request): # Views para la home page
    cancionesQuery = Cancion.objects.all()
    cancionGusto = recomByLikes(request)

    canciones = []
    for cancion in cancionesQuery:
        dictio = {"nombre":cancion.nombre,
        "audio": cancion.audio.url,
        "imagen": cancion.imagen,
        "duracion": cancion.duracion
        }
        canciones.append(dictio)

    cancionesGusto = []
    for cancion in cancionGusto:
        dictio = {"nombre":cancion.nombre,
        "audio": cancion.audio.url,
        "imagen": cancion.imagen,
        "duracion": cancion.duracion
        }
        cancionesGusto.append(dictio)

    contexto = {'canciones':canciones, 'cancionesGusto':cancionesGusto}
    return render(request, template_name='home.html', context=contexto)

# función para recomendar por gustos
def recomByLikes(request):
    gustos=Genero_Favorito.objects.filter(id_perfil__usuario=request.user)
    gustos=[gusto.id_genero.nombre for gusto in gustos] 

    cancionesPosibles=Genero_Cancion.objects.filter(id_genero__nombre__in=gustos)
    canciones=[]

    while(len(canciones)<15 and cancionesPosibles.count()>0):
        cancion = random.choice(cancionesPosibles)
        canciones.append(cancion.id_cancion)
        cancionesPosibles=cancionesPosibles.exclude(id_cancion__nombre__exact=cancion.id_cancion.nombre)

    return canciones


@login_required(login_url='/login/')
def miPerfil_page(request):
    usuario = User.objects.get(id=request.user.id) #Obtener usuario logeado
    perfil = Perfil.objects.get(usuario=usuario.id) #Obtener perfil segun el usuario logeado

    nombreCompleto = usuario.first_name + " " + usuario.last_name
    fechaNacimiento = perfil.fecha_nacimiento
    fechaUnido = usuario.date_joined
    nombreUsuario = usuario.username
    correo = usuario.email

    info ={
        'nombre': nombreCompleto,
        'fechaNacimiento': fechaNacimiento,
        'fechaUnido': fechaUnido,
        'nombreUsuario': nombreUsuario,
        'correo': correo,
    }
    
    context={'info': info}
    return render(request, template_name='miPerfil.html',context=context)

@login_required(login_url='/login/')
def tuMusica_page(request): 
    return render(request, template_name='tuMusica.html')

@login_required(login_url='/login/')
def formsFellings_page(request):

    usuario = User.objects.get(id=request.user.id) #Obtener usuario logeado
    perfil = Perfil.objects.get(usuario=usuario.id) #Obtener perfil segun el usuario logeado

    if request.method == 'POST':

        genFav = request.POST.getlist('genFav')
        genFel = request.POST.getlist('genFel')
        genTri = request.POST.getlist('genTri')
        genEno = request.POST.getlist('genEno')

        if((genFav != []) and (genFel != []) and (genTri != []) and (genEno != [])):

            genFavAct = Genero_Favorito.objects.filter(id_perfil=perfil.id)
            genFelAct = Genero_Feliz.objects.filter(id_perfil=perfil.id)
            genTriAct = Genero_Triste.objects.filter(id_perfil=perfil.id)
            genEnoAct = Genero_Enojado.objects.filter(id_perfil=perfil.id)

            # Borra si tiene anteriormente creadas

            if (genFavAct is not None):
                for gen in genFavAct:
                    gen.delete()

            if (genFelAct is not None):
                for gen in genFelAct:
                    gen.delete()

            if (genTriAct is not None):
                for gen in genTriAct:
                    gen.delete()
            
            if (genEnoAct is not None):
                for gen in genEnoAct:
                    gen.delete()

            ############ Agrega las nuevas canciones ####################

            for i in range(len(genFav)):
                gen = Genero.objects.get(id=int(genFav[i]))
                a = Genero_Favorito(id_genero=gen,id_perfil=perfil)
                a.save()

            for i in range(len(genFel)):
                gen = Genero.objects.get(id=int(genFel[i]))
                a = Genero_Feliz(id_genero=gen,id_perfil=perfil)
                a.save()

            for i in range(len(genTri)):
                gen = Genero.objects.get(id=int(genTri[i]))
                a = Genero_Triste(id_genero=gen,id_perfil=perfil)
                a.save()

            for i in range(len(genEno)):
                gen = Genero.objects.get(id=int(genEno[i]))
                a = Genero_Enojado(id_genero=gen,id_perfil=perfil)
                a.save()

            messages.success(request, '¡La información se guardo exitosamente!')
            return redirect('home')
        else:
            messages.success(request, '¡Por favor llene todos los campos!')

    generos = Genero.objects.all().order_by('nombre').values()
    context = {'generos':generos}
    return render(request, template_name='formsFellings.html',context=context)

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
            messages.success(request, f'¡Bienvenido {user.username}, nos encanta tenerte de vuelta!')
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
    cancionesQuery=[]
    
    if(userEmotion=="feliz"):
        gustos=Genero_Feliz.objects.filter(id_perfil__usuario=request.user)
        gustos=[gusto.id_genero.nombre for gusto in gustos]

        cancionesPosibles=Genero_Cancion.objects.filter(id_genero__nombre__in=gustos)

        listaGustos=[cancionPosible.id_cancion.nombre for cancionPosible in cancionesPosibles]
        print(listaGustos)
        #gustos cuando está feliz

        CancionesAltas=Cancion.objects.filter(nombre__in=listaGustos).filter(frecuencia__in=[4,5]).filter(intensidad_feliz__gte=F('intensidad_enojo')).filter(intensidad_enojo__gte=F('intensidad_triste'))
        #Filtro:
        #frecuencias 4 y 5
        # %Feliz >= %Enojo >= %Triste
        CancionesNeutras=Cancion.objects.filter(nombre__in=listaGustos).filter(frecuencia__in=[3]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 3
        # 20% < %Feliz %Triste Y %Enojo < 45%
        
        while(len(cancionesQuery)<4 and CancionesAltas.count()>0):
            cancion = random.choice(CancionesAltas)
            cancionesQuery.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(cancionesQuery)<5 and CancionesNeutras.count()>0):
            cancion = random.choice(CancionesNeutras)
            cancionesQuery.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(cancionesQuery)<9 and CancionesAltas.count()>0):
            cancion = random.choice(CancionesAltas)
            cancionesQuery.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(cancionesQuery)<10 and CancionesNeutras.count()>0):
            cancion = random.choice(CancionesNeutras)
            cancionesQuery.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(cancionesQuery)<14 and CancionesAltas.count()>0):
            cancion = random.choice(CancionesAltas)
            cancionesQuery.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)
        
        while(len(cancionesQuery)<15 and CancionesNeutras.count()>0):
            cancion = random.choice(CancionesNeutras)
            cancionesQuery.append(cancion)
            CancionesAltas=CancionesAltas.exclude(nombre__exact=cancion.nombre)
            CancionesNeutras=CancionesNeutras.exclude(nombre__exact=cancion.nombre)        

    elif(userEmotion=="triste"):
        gustos=Genero_Triste.objects.filter(id_perfil__usuario=request.user)
        gustos=[gusto.id_genero.nombre for gusto in gustos]

        cancionesPosibles=Genero_Cancion.objects.filter(id_genero__nombre__in=gustos)
        
        listaGustos=[cancionPosible.id_cancion.nombre for cancionPosible in cancionesPosibles]
        print(listaGustos)
        #gustos cuando está triste
        
        CancionesEmpatia=Cancion.objects.filter(nombre__in=listaGustos).filter(frecuencia__in=[4,3,2]).filter(intensidad_triste__gte=F('intensidad_feliz')).filter(intensidad_feliz__gte=F('intensidad_enojo'))
        #Filtro:
        #frecuencias 4,3,2
        # %Triste >= %Feliz >= %Enojo
        CancionesMedio=Cancion.objects.filter(nombre__in=listaGustos).filter(frecuencia__in=[3,2]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 3,2
        # 20% < %Feliz %Triste Y %Enojo < 45%
        CancionesSuave=Cancion.objects.filter(nombre__in=listaGustos).filter(frecuencia__in=[2,1]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 2,1
        # 20% < %Feliz %Triste Y %Enojo < 45%

        while(len(cancionesQuery)<5 and CancionesEmpatia.count()>0):
            cancion = random.choice(CancionesEmpatia)
            cancionesQuery.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)
        
        while(len(cancionesQuery)<10 and CancionesMedio.count()>0):
            cancion = random.choice(CancionesMedio)
            cancionesQuery.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)

        while(len(cancionesQuery)<15 and CancionesSuave.count()>0):
            cancion = random.choice(CancionesSuave)
            cancionesQuery.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)
    
    elif(userEmotion=="enojado"):
        gustos=Genero_Favorito.objects.filter(id_perfil__usuario=request.user)
        gustos=[gusto.id_genero.nombre for gusto in gustos]

        cancionesPosibles=Genero_Cancion.objects.filter(id_genero__nombre__in=gustos)

        listaGustos=[cancionPosible.id_cancion.nombre for cancionPosible in cancionesPosibles]
        print(listaGustos)
        #gustos cuando está enojado

        CancionesEmpatia=Cancion.objects.filter(nombre__in=listaGustos).filter(frecuencia__in=[5,4,3]).filter(intensidad_enojo__gte=F('intensidad_feliz')).filter(intensidad_feliz__gte=F('intensidad_triste'))
        #Filtro:
        #frecuencias 5,4,3
        # %Enojo >= %Feliz >= %Triste
        CancionesMedio=Cancion.objects.filter(nombre__in=listaGustos).filter(frecuencia__in=[3,2]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 3,2
        # 20% < %Feliz %Triste Y % Enojo < 45%
        CancionesSuave=Cancion.objects.filter(nombre__in=listaGustos).filter(frecuencia__in=[2,1]).filter(intensidad_feliz__range=(20,45)).filter(intensidad_triste__range=(20,45)).filter(intensidad_enojo__range=(20,45))
        #Filtro:
        #frecuencia 2,1
        # 20% < %Feliz %Triste Y % Enojo < 45%
        
        while(len(cancionesQuery)<5 and CancionesEmpatia.count()>0):
            cancion = random.choice(CancionesEmpatia)
            cancionesQuery.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)
        
        while(len(cancionesQuery)<10 and CancionesMedio.count()>0):
            cancion = random.choice(CancionesMedio)
            cancionesQuery.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)

        while(len(cancionesQuery)<15 and CancionesSuave.count()>0):
            cancion = random.choice(CancionesSuave)
            cancionesQuery.append(cancion)
            CancionesEmpatia=CancionesEmpatia.exclude(nombre__exact=cancion.nombre)
            CancionesMedio=CancionesMedio.exclude(nombre__exact=cancion.nombre)
            CancionesSuave=CancionesSuave.exclude(nombre__exact=cancion.nombre)

    canciones = []
    for cancion in cancionesQuery:
        dictio = {"nombre":cancion.nombre,
        "audio": cancion.audio.url,
        "imagen": cancion.imagen,
        "duracion": cancion.duracion
        }
        canciones.append(dictio)

    context={'userEmotion':userEmotion,'canciones':canciones,'MOOD':True}
    #parametros:
    #userEmotion: la emoción que mandaremis a la playlist
    #canciones: la lista de las canciones
    #MOOD: el verificador que ya se usó el servicio de mood para poder enviar la encuesta

    return render(request, template_name='playlist.html', context = context)

def sendSatisfactionForm(request,goto):
    #Guardamos los datos que ingresaremos en las persistencias
    usuario= request.user
    fecha=datetime.now()
    calificacion=request.GET["punctuation"]

    #Ingreso CSV (abrimos el csv en modo append)
    fileCsv=open('main\data\SatisfactionFormMood.csv','a',newline='\n')

    escritor=csv.writer(fileCsv)
    escritor.writerow([usuario,fecha,calificacion])

    fileCsv.close()

    #Ingreso JSON (abrimos el json en modo append)
    fileJson=open('main\data\SatisfactionFormMood.json','r+')

    dataJson=json.load(fileJson)
    dataJson.append({"usuario":str(usuario),"fecha":str(fecha),"calificacion":calificacion})
    fileJson.seek(0)
    json.dump(dataJson,fileJson,indent=2)

    fileJson.close()

    #redirigimos a la pestaña a la que el usuario buscaba ir
    if(goto=="home"):
        return home_page(request)
    elif(goto=="mood"):
        return mood_page(request)
    elif(goto=="tumusica"):
        return tuMusica_page(request)
    elif(goto=="perfil"):
        return miPerfil_page(request)

# @login_required(login_url='/login/')
# def logout_view(request):
#     logout(request)
#     messages.success(request, f'Sesión cerrada correctamente')
#     return login_page(request)

#--------------------------------------------- utilidad para guardar musica en la BBDD -------------------------------
def SubirMusica(request):
    archivo = open("main/data/help.csv",encoding="UTF-8")
    verificacion=[]
    for linea in archivo:
        registro= linea.split(";")    
        registro[-1]=registro[-1][:-1] #quitamos el /n --> ojo que la última linea si tenga salto porque sino se daña
        #registro[0] nombre
        #registro[1] duracion
        #registro[2] frecuencia
        #registro[3] idioma
        #registro[4] intensidad feliz
        #registro[5] intensidad triste
        #registro[6] intensidad enojado
        #registro[7] generos
        #registro[8] artistas

        #Canción
        if(len(Cancion.objects.filter(nombre=registro[0].title()))==0):
            cancionSV=Cancion(nombre=registro[0].title(),duracion=int(registro[1]),frecuencia=int(registro[2]),idioma=registro[3].title(),intensidad_feliz=int(registro[4]),intensidad_triste=int(registro[5]),intensidad_enojo=int(registro[6]))
            cancionSV.save()

        can=Cancion.objects.get(nombre=registro[0].title())

        #Géneros
        registro[7]=registro[7].split(",")
        #Ya están los géneros?
        for genero in registro[7]:
            if(len(Genero.objects.filter(nombre=genero.title()))==0):
                generoSV=Genero(nombre=genero.title())
                generoSV.save()

            #Vinculo
            
            gen=Genero.objects.get(nombre=genero.title())
            RelGC = Genero_Cancion(id_genero=gen,id_cancion=can)
            RelGC.save()

        #Artistas
        registro[8]=registro[8].split(",")
        #Ya están los artistas?
        for artista in registro[8]:
            if(len(Artista.objects.filter(nombre=artista.title()))==0):
                artistaSV=Artista(nombre=artista.title())
                artistaSV.save()
       
            #Vinculo
            art=Artista.objects.get(nombre=artista.title())
            RelAC = Artista_Cancion(id_artista=art,id_cancion=can)
            RelAC.save()

        verificacion.append(registro[0].title)
        print(registro)

    archivo.close()

    return render(request,template_name="zzVerificar.html",context={"lista":verificacion})

def subirDuracion(request):
    archivo = open("main/data/help.csv",encoding="UTF-8")

    verificacion=[]

    for linea in archivo:
        registro= linea.split(";")    
        registro[-1]=registro[-1][:-1]

        cancionAct = Cancion.objects.get(nombre=registro[0])
        cancionAct.duracion=int(registro[1])
        cancionAct.save()

        mistr=registro[0]+"que dura: "+registro[1]
        verificacion.append(mistr)

    archivo.close()
    return render(request,template_name="zzVerificar.html",context={"lista":verificacion})

def subirAudios(request):
    archivo = open("main/data/help.csv",encoding="UTF-8")

    verificacion=[]

    for linea in archivo:
        registro= linea.split(";")    
        registro[-1]=registro[-1][:-1]

        cancionAct = Cancion.objects.get(nombre=registro[0])
        #opción 1
        cancionAct.audio="audios/"+registro[1]#ojo que debe incluir el .mp3 en el excel
        #opción 2
        #cancionAct.audio="audios/"+registro[0].lower().replace(" ","_")+".mp3"
        cancionAct.save()

        mistr=registro[0]+"con la direccion: audios/"+registro[1]
        verificacion.append(mistr)

    archivo.close()
    return render(request,template_name="zzVerificar.html",context={"lista":verificacion})