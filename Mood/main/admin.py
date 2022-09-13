from django.contrib import admin

from main.models import Artista,Artista_Cancion,Cancion,Genero,Genero_Cancion,Perfil,Playlist,Playlist_Cancion,Genero_Favorito,Genero_Feliz,Genero_Triste,Genero_Enojado

class ArtistaAdmin(admin.ModelAdmin):
    list_display=("nombre",)
    search_fields=("nombre",)
    list_filter=("nombre",)

class Artista_CancionAdmin(admin.ModelAdmin):
    list_display=("id_artista","id_cancion")
    search_fields=("id_artista","id_cancion")
    list_filter=("id_artista","id_cancion")

class CancionAdmin(admin.ModelAdmin):
    list_display=("nombre","audio","imagen","duracion", "frecuencia","idioma","intensidad_feliz","intensidad_triste","intensidad_enojo")
    search_fields=("nombre","duracion", "frecuencia","idioma")
    list_filter=("nombre","duracion", "frecuencia","idioma")

class GeneroAdmin(admin.ModelAdmin):
    list_display=("nombre",)
    search_fields=("nombre",)
    list_filter=("nombre",)

class Genero_CancionAdmin(admin.ModelAdmin):
    list_display=("id_genero","id_cancion")
    search_fields=("id_genero","id_cancion")
    list_filter=("id_genero","id_cancion")

class Genero_FavoritoAdmin(admin.ModelAdmin):
    list_display=("id_genero","id_perfil")
    search_fields=("id_genero","id_perfil")
    list_filter=("id_genero","id_perfil")

class Genero_FelizAdmin(admin.ModelAdmin):
    list_display=("id_genero","id_perfil")
    search_fields=("id_genero","id_perfil")
    list_filter=("id_genero","id_perfil")

class Genero_TristeAdmin(admin.ModelAdmin):
    list_display=("id_genero","id_perfil")
    search_fields=("id_genero","id_perfil")
    list_filter=("id_genero","id_perfil")

class Genero_EnojadoAdmin(admin.ModelAdmin):
    list_display=("id_genero","id_perfil")
    search_fields=("id_genero","id_perfil")
    list_filter=("id_genero","id_perfil")

class PerfilAdmin(admin.ModelAdmin):
    list_display=("usuario","fecha_nacimiento")
    search_fields=("usuario","fecha_nacimiento")
    list_filter=("usuario","fecha_nacimiento")

class PlaylistAdmin(admin.ModelAdmin):
    list_display=("id_perfil","nombre")
    search_fields=("id_perfil","nombre")
    list_filter=("id_perfil","nombre")

class Playlist_CancionAdmin(admin.ModelAdmin):
    list_display=("id_playlist","id_cancion")
    search_fields=("id_playlist","id_cancion")
    list_filter=("id_playlist","id_cancion")

admin.site.register(Artista, ArtistaAdmin)
admin.site.register(Artista_Cancion, Artista_CancionAdmin)
admin.site.register(Cancion, CancionAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Genero_Cancion, Genero_CancionAdmin)
admin.site.register(Genero_Favorito, Genero_FavoritoAdmin)
admin.site.register(Genero_Feliz, Genero_FelizAdmin)
admin.site.register(Genero_Triste, Genero_TristeAdmin)
admin.site.register(Genero_Enojado, Genero_EnojadoAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Playlist_Cancion, Playlist_CancionAdmin)