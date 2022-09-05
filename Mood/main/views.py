from re import template
from urllib import request
from django.shortcuts import render,redirect
import matplotlib.pyplot as plt
import cv2
from deepface import DeepFace
import numpy as np
from main.models import Sentimiento_Cancion

# Create your views here.

def regsiter_page(request):
    return render(request, template_name='registro.html')

def home_page(request): # Views para la home page
    return render(request, template_name='home.html')


def mood_page(request): #Views para la pagina mood
    return render(request, template_name='mood.html')


def recognize(request): #Views para la pagina mood

    print("estoy entrando")

    userEmotion = "" #initialize empty variable 
    faceCascadeName = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'  #getting a haarcascade xml file
    faceCascade = cv2.CascadeClassifier()  #processing it for our project
    if not faceCascade.load(cv2.samples.findFile(faceCascadeName)):  #adding a fallback event
        print("Error loading xml file")

    video=cv2.VideoCapture(0)  #requisting the input from the webcam or camera

    while video.isOpened():  #checking if are getting video feed and using it
        _,frame = video.read()

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  #changing the video to grayscale to make the face analisis work properly
        face=faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)

        for x,y,w,h in face:
            img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)  #making a recentangle to show up and detect the face and setting it position and colour
        
            #making a try and except condition in case of any errors
            try:
                analyze = DeepFace.analyze(frame)  #same thing is happing here as the previous example, we are using the analyze class from deepface and using ‘frame’ as input
                userEmotion = analyze['dominant_emotion']

            except:
                userEmotion = " "

            #this is the part where we display the output to the user
            cv2.imshow('video', frame)
            key=cv2.waitKey(1) 
            if key==ord('q'):   # here we are specifying the key which will stop the loop and stop all the processes going
                break
        video.release()

        if userEmotion == "happy" or userEmotion == "neutral" or userEmotion == "surprised":
            userEmotion = "feliz"

        elif userEmotion == "sad" or userEmotion == "fear":
            userEmotion = "triste"

        elif userEmotion == "angry" or userEmotion == "disgust":
            userEmotion = "enojado"
            
        else:
            userEmotion = "No reconocio tu cara, vuelve a intentarlo"

    print(userEmotion)

    canciones = Sentimiento_Cancion.objects.filter(id_sentimiento__nombre__contains=userEmotion)

    context={'userEmotion':userEmotion,'canciones':canciones}

    return render(request, template_name='mood.html', context=context)
