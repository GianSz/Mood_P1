from cgitb import handler
from django.urls import path # Como este es un archivo creado por mi, yo mismo pongo la importación
from main import views
from django.contrib.auth.views import logout_then_login
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home_page, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),
    path('mood/', views.mood_page, name='mood'),
    path('mood/texto/', views.moodByText, name='texto'),
    path('mood/camara/', views.moodByCamera, name='camara'),
    path('recognize/', views.recognize, name='recognize'),
    path('miPerfil/',views.miPerfil_page, name='miPerfil'),
    path('tuMusica/',views.tuMusica_page, name='tuMusica'),
    path('formsFellings/',views.formsFellings_page, name='formsFellings'),
    path('get-songs/', views.get_song),
    path('playlist/<str:userEmotion>', views.playlist, name = 'playlist'),
    path('logout/', logout_then_login, name='logout'),
    path('sendSatisfactionForm/<str:goto>', views.sendSatisfactionForm, name='sendSatisfactionForm'),#recibe la página a la que se debe redireccionar
    path('terminosycondiciones/', views.terminos, name='terminos'),
    # Las siguientes deberán tener alguna seguridad para que los usuarios no puedan acceder a ellas
    path('musicaBD', views.SubirMusica, name='subirMusica'),#utilidad pa subir a la BBDD
    path('duracionBD', views.subirDuracion, name='subirDuracion'),#utilidad pa subir a la BBDD
    path('audiosBD', views.subirAudios, name='subirAudios'),#utilidad pa subir a la BBDD
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "main.views.handle_not_found"