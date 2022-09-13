from django.db import models
from django.contrib.auth.models import User

# Definimos los modelos.

class Perfil(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"
        db_table = "perfil"

    def __str__(self):
        return str(self.usuario.username)

class Cancion(models.Model):
    nombre=models.CharField(max_length=25, null=False,blank=False)
    audio=models.CharField(max_length=50, null=True,blank=True)
    imagen=models.CharField(max_length=50,null=True,blank=True)
    duracion=models.TimeField(null=False,blank=False)
    frecuencia=models.IntegerField(null=True,blank=True)
    idioma=models.CharField(max_length=15,null=False,blank=False)
    intensidad_feliz=models.IntegerField(null=True,blank=True)
    intensidad_triste=models.IntegerField(null=True,blank=True)
    intensidad_enojo=models.IntegerField(null=True,blank=True)

    class Meta:
        verbose_name = "cancion"
        verbose_name_plural = "canciones"
        db_table = "cancion"

    def __str__(self):
        return (self.nombre)

class Playlist(models.Model):
    id_perfil=models.ForeignKey(Perfil,null=False,blank=False,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=25, null=False,blank=False)
   
    class Meta:
        verbose_name = "playlist"
        verbose_name_plural = "playlists"
        db_table = "playlist"

    def __str__(self):
        return (self.nombre)

class Playlist_Cancion(models.Model):
    id_playlist=models.ForeignKey(Playlist,null=False,blank=False,on_delete=models.CASCADE)
    id_cancion=models.ForeignKey(Cancion,null=False,blank=False,on_delete=models.CASCADE)
   
    class Meta:
        verbose_name = "playlist_cancion"
        verbose_name_plural = "playlist_canciones"
        db_table = "playlist_cancion"

    def __str__(self):
        return (self.id_cancion+" en "+self.id_playlist)

class Artista(models.Model):
    nombre=models.CharField(max_length=25, null=False,blank=False)

    class Meta:
        verbose_name = "artista"
        verbose_name_plural = "artistas"
        db_table = "artista"

    def __str__(self):
        return (self.nombre)

class Artista_Cancion(models.Model):
    id_artista=models.ForeignKey(Artista,null=False,blank=False,on_delete=models.CASCADE)
    id_cancion=models.ForeignKey(Cancion,null=False,blank=False,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "artista_cancion"
        verbose_name_plural = "artista_canciones"
        db_table = "artista_cancion"

    def __str__(self):
        return (self.id_cancion.nombre+" de "+self.id_artista.nombre)

class Genero(models.Model):
    nombre=models.CharField(max_length=25, null=False,blank=False)

    class Meta:
        verbose_name = "genero"
        verbose_name_plural = "generos"
        db_table = "genero"

    def __str__(self):
        return (self.nombre)

class Genero_Cancion(models.Model):
    id_genero=models.ForeignKey(Genero,null=False,blank=False,on_delete=models.CASCADE)
    id_cancion=models.ForeignKey(Cancion,null=False,blank=False,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "genero_cancion"
        verbose_name_plural = "genero_canciones"
        db_table = "genero_cancion"

    def __str__(self):
        return (self.id_cancion.nombre+" gen:"+self.id_genero.nombre)

class Genero_Favorito(models.Model):
    id_genero=models.ForeignKey(Genero,null=False,blank=False,on_delete=models.CASCADE)
    id_perfil=models.ForeignKey(Perfil,null=False,blank=False,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "genero_favorito"
        verbose_name_plural = "generos_favoritos"
        db_table = "genero_favorito"

    def __str__(self):
        return (self.id_perfil.usuario.username+" gen:"+self.id_genero.nombre)

class Genero_Triste(models.Model):
    id_genero=models.ForeignKey(Genero,null=False,blank=False,on_delete=models.CASCADE)
    id_perfil=models.ForeignKey(Perfil,null=False,blank=False,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "genero_triste"
        verbose_name_plural = "generos_tristes"
        db_table = "genero_triste"

    def __str__(self):
        return (self.id_perfil.usuario.username+" gen:"+self.id_genero.nombre)

class Genero_Feliz(models.Model):
    id_genero=models.ForeignKey(Genero,null=False,blank=False,on_delete=models.CASCADE)
    id_perfil=models.ForeignKey(Perfil,null=False,blank=False,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "genero_feliz"
        verbose_name_plural = "generos_felices"
        db_table = "genero_feliz"

    def __str__(self):
        return (self.id_perfil.usuario.username+" gen:"+self.id_genero.nombre)

class Genero_Enojado(models.Model):
    id_genero=models.ForeignKey(Genero,null=False,blank=False,on_delete=models.CASCADE)
    id_perfil=models.ForeignKey(Perfil,null=False,blank=False,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "genero_enojado"
        verbose_name_plural = "generos_enojados"
        db_table = "genero_enojado"

    def __str__(self):
        return (self.id_perfil.usuario.username+" gen:"+self.id_genero.nombre)


