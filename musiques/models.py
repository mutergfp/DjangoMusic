from django.db import models
from datetime import date, timedelta
# Create your models here.

TYPE_ALBUM = (
    ('EP', 'EP'),
    ('AL', 'Album'),
    ('SG', 'Single')
)
class Artiste(models.Model):
    nom_artiste = models.CharField(verbose_name=("Nom de l'artiste"), max_length=255, null=False)
    description_artiste = models.TextField(verbose_name=("Description de l'artiste"), null=True)
<<<<<<< HEAD
    image_artiste = models.ImageField(verbose_name=("Image de l'artiste"), upload_to="assets/img_albums", null=True, default="static/default/img_artiste_default-min.jpg")
=======
    image_artiste = models.ImageField(verbose_name=("Image de l'artiste"), upload_to="assets/img_albums", null=True, default="assets/default/img_artiste_default-min.jpg")
>>>>>>> developLucas

    def __str__(self):
        return self.nom_artiste

class Label(models.Model):
    nom_label = models.CharField(verbose_name=("Nom du Label"), max_length=100, null=False)
    description_label = models.TextField(verbose_name=("Description du Label"), null=True)

    def __str__(self):
        return self.nom_label

class Genre(models.Model):
    nom_genre = models.CharField(verbose_name=("Nom du genre"), max_length=100)
    description_genre = models.CharField(verbose_name=("Description du genre"), max_length=50)

    def __str__(self):
        return self.nom_genre

class Album(models.Model):
    nom_album = models.CharField(verbose_name=("Nom de la l'album"), max_length=100)
    type_album = models.CharField(verbose_name=("Type de l'album"), max_length=6, choices=TYPE_ALBUM)
<<<<<<< HEAD
    image_album = models.ImageField(verbose_name=("Image de l'album"), upload_to="assets/img_artistes", null=False, default="static/assets/default/img_album_default-min.jpg")
=======
    image_album = models.ImageField(verbose_name=("Image de l'album"), upload_to="assets/img_artistes", null=False, default="assets/default/img_album_default-min.jpg")
>>>>>>> developLucas
    date_publication_album = models.DateField(verbose_name=("Date de parution de l'album"), null=True)
    id_artiste = models.ForeignKey(Artiste, verbose_name=("Artiste de l'album"), on_delete=models.CASCADE, null=False)
    id_label = models.ForeignKey(Label, verbose_name=("Label de l'album"), on_delete=models.CASCADE, null=False)
    id_genre = models.ForeignKey(Genre, verbose_name=("Genre de l'album"), on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.nom_album + ' (' + str(self.date_publication_album.year) + ')'

class Musique(models.Model):
    titre_musique = models.CharField(verbose_name=("Titre de la musique"), max_length=255, null=False)
    duree_musique = models.CharField(verbose_name=("Durée de la musique (MM:SS)"), max_length=6, null=False)
    #Relation ManyToMany ATTENTION
    id_artiste = models.ManyToManyField(Artiste, verbose_name=("Artiste(s) de la musique"))
    id_album = models.ForeignKey(Album, verbose_name=("Album de la musiques"), on_delete=models.CASCADE, related_name="albums")

    def __str__(self):
        return self.titre_musique