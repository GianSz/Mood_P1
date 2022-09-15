from django.urls import path # Como este es un archivo creado por mi, yo mismo pongo la importación
from main import views
from django.contrib.auth.views import logout_then_login
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home_page, name='home'), # Esta se debe cambiar a que dirija al login de primerazo
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),
    path('mood/', views.mood_page, name='mood'),
    path('recognize/', views.recognize, name='recognize'),
    path('miPerfil/',views.miPerfil_page, name='miPerfil'),
    path('tuMusica/',views.tuMusica_page, name='tuMusica'),
    path('formsFellings/',views.formsFellings_page, name='formsFellings'),
    path('get-songs/', views.get_song),
    path('playlist/<str:userEmotion>', views.playlist, name = 'playlist'),
    path('logout/', logout_then_login, name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)