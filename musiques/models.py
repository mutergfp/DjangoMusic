from django.db import models
from datetime import date, timedelta
from django.contrib.auth.models import User
# Create your models here.

TYPE_ALBUM = (
    ('EP', 'EP'),
    ('AL', 'Album'),
    ('SG', 'Single')
)
class Artiste(models.Model):
    nom_artiste = models.CharField(verbose_name=("Nom de l'artiste"), max_length=255, null=False)
    description_artiste = models.TextField(verbose_name=("Description de l'artiste"), null=True, default="Pas de description disponnible pour cet artiste.")
    image_artiste = models.ImageField(verbose_name=("Image de l'artiste"), upload_to="assets/img_albums", null=True, default="assets/default/img_artiste_default-min.jpg")
    spotify_id_artiste = models.TextField(verbose_name=("ID Spotify de l'artiste"), null=True)
    def __str__(self):
        return self.nom_artiste

class Genre(models.Model):
    nom_genre = models.CharField(verbose_name=("Nom du genre"), max_length=100)
    description_genre = models.CharField(verbose_name=("Description du genre"), max_length=50)

    def __str__(self):
        return self.nom_genre
        
class Album(models.Model):
    nom_album = models.CharField(verbose_name=("Nom de la l'album"), max_length=100)
    type_album = models.CharField(verbose_name=("Type de l'album"), max_length=6)
    image_album = models.ImageField(verbose_name=("Image de l'album"), upload_to="assets/img_artistes", null=False, default="assets/default/img_album_default-min.jpg")
    date_publication_album = models.CharField(verbose_name=("Date de parution de l'album"), null=True, max_length=10)
    id_artiste = models.ForeignKey(Artiste, verbose_name=("Artiste de l'album"), on_delete=models.CASCADE, null=False)
    spotify_id_album = models.TextField(verbose_name=("ID Spotify de l'album"), null=True)
    id_genre = models.ForeignKey(Genre, verbose_name=("Genre de l'album"), on_delete=models.CASCADE, null=False)
    lien_album = models.TextField(verbose_name=("Lien de l'album sur AllForMusic"), null=True)
    def __str__(self):
        return self.nom_album

class Musique(models.Model):
    titre_musique = models.CharField(verbose_name=("Titre de la musique"), max_length=255, null=False)
    duree_musique = models.CharField(verbose_name=("Durée de la musique (MM:SS)"), max_length=6, null=False)
    #Relation ManyToMany ATTENTION
    id_artiste = models.ManyToManyField(Artiste, verbose_name=("Artiste(s) de la musique"))
    id_album = models.ForeignKey(Album, verbose_name=("Album de la musiques"), on_delete=models.CASCADE, related_name="albums")

    def __str__(self):
        return self.titre_musique

class Recherche(models.Model):
    contenu_recherche = models.CharField(verbose_name=("Contenu de la recherche"), max_length=255, null=False)
    compteur_recherche = models.IntegerField(verbose_name=("Nombre de fois"), null=False, default=1)

class Playlist(models.Model):
    nom_playlist = models.CharField(verbose_name=("Nom de la playlist"), max_length=50, null=False)
    image_playlist = models.ImageField(verbose_name=("Image de la playlist"), upload_to="assets/img_playlists", default="/assets/default/img_album_default-min.jpg")
    id_user = models.ForeignKey(User, verbose_name=("Utilisateur de la playlist"), on_delete=models.CASCADE)
    id_musique = models.ManyToManyField(Musique, verbose_name=("Musique de la playlist"))
