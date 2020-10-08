from django.contrib import admin
from musiques.models import Artiste, Label, Genre, Album, Musique

# Register your models here.
class ArtisteAdmin(admin.ModelAdmin):
    list_display=('nom_artiste', 'description_artiste', 'image_artiste')

class LabelAdmin(admin.ModelAdmin):
    list_display=('nom_label', 'description_label')

class GenreAdmin(admin.ModelAdmin):
    list_display=('nom_genre', 'description_genre')

class AlbumAdmin(admin.ModelAdmin):
    list_display=('nom_album', 'type_album', 'image_album', 'date_publication_album')

class MusiqueAdmin(admin.ModelAdmin):
    list_display=('titre_musique', 'duree_musique')

admin.site.register(Artiste, ArtisteAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Musique, MusiqueAdmin)

    
