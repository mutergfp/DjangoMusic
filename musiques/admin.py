from django.contrib import admin
from musiques.models import Artiste, Genre, Album, Musique, Recherche, Playlist


# Register your models here.
class ArtisteAdmin(admin.ModelAdmin):
    list_display=('id', 'nom_artiste', 'description_artiste', 'image_artiste', 'spotify_id_artiste')

class AlbumAdmin(admin.ModelAdmin):
    list_display=('id', 'nom_album', 'type_album', 'image_album', 'date_publication_album', 'spotify_id_album')

class MusiqueAdmin(admin.ModelAdmin):
    list_display=('titre_musique', 'duree_musique')

class RechercheAdmin(admin.ModelAdmin):
    list_display=('contenu_recherche', 'compteur_recherche')

class PlaylistAdmin(admin.ModelAdmin):
    list_display=('nom_playlist', 'image_playlist')

class GenreAdmin(admin.ModelAdmin):
    list_display=('nom_genre', 'description_genre')
    
admin.site.register(Artiste, ArtisteAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Musique, MusiqueAdmin)
admin.site.register(Recherche, RechercheAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Genre, GenreAdmin)
