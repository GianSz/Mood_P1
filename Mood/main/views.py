from urllib import request
from django.shortcuts import render,redirect
import matplotlib.pyplot as plt
import cv2
from deepface import DeepFace
import numpy as np
from main.models import Sentimiento_Cancion

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
