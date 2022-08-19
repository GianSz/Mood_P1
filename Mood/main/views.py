from urllib import request
from django.shortcuts import render,redirect
import matplotlib.pyplot as plt
import cv2
from deepface import DeepFace
import numpy as np
from main.models import Sentimiento_Cancion

# Create your views here.

def home_page(request): # Views para la home page
    return render(request, template_name='home.html')


def mood_page(request): #Views para la pagina mood
    return render(request, template_name='mood.html')


def recognize(request): #Views para la pagina mood

    print("estoy entrando")

    userEmotion = "" #initialize empty variable for storing the users emotion
    faceCascadeName = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'  #getting a haarcascade xml file for recognizing faces
    faceCascade = cv2.CascadeClassifier()  #processing it for detecting faces
    if not faceCascade.load(cv2.samples.findFile(faceCascadeName)):  #in case the file is not correctly downloaded
        print("Error loading xml file")

    video=cv2.VideoCapture(0)  #requisting the input from the webcam or camera

    while video.isOpened():  #verifying if the camera was opened
        _,frame = video.read() #read the camera footage

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  #converting the live footage to a gray scale so the recognition is more accurate and easy to detect
        face=faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5) 

             
        #we'll do a try and exception to analyze the users emotion
        try:
            #if we can detect a face we use DeepFace.analyze to extract the information (emtion, age, race and) of the user
            analyze = DeepFace.analyze(frame) 
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
            userEmotion = "No reconocio tu cara, vuelve a intentarlo"

    print(userEmotion)

    canciones = Sentimiento_Cancion.objects.filter(id_sentimiento__nombre__contains=userEmotion)

    context={'userEmotion':userEmotion,'canciones':canciones}

    return render(request, template_name='mood.html', context=context)
