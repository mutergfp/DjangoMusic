from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Artiste, Musique, Album, Recherche, Genre
from django import forms
from musiques.functions.utils import *


# Create your views here.

class RechercheForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RechercheForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    search = forms.CharField(max_length=250)

def index(request):
    if(request.method == "POST"):
        form = RechercheForm(request.POST)
        if(form.is_valid()):
            return redirect('search/'+request.POST['search'])
    else:
        search_form = RechercheForm()
        return render(request, 'index.html', {'search': search_form})

def resultSearch(request, text=None):

    if(text != None):
        try: 
            issetRecherche = Recherche.objects.get(contenu_recherche = text)
        except Recherche.DoesNotExist:
            spotify_create_artiste(text)
        else:
            issetRecherche.compteur_recherche += 1
            issetRecherche.save()

        try:
            resultArtiste = Artiste.objects.filter(nom_artiste__contains = text)
        except Artiste.DoesNotExist:
            resultArtiste = "Aucun résultat trouvé"

        try:
            resultAlbum = Album.objects.filter(nom_album__contains=text)
        except Album.DoesNotExist:
            resultAlbum = "Aucun résultat trouvé"

        try:
            resultMusique = Musique.objects.filter(titre_musique__contains=text)
        except:
            resultMusique = "Aucun résultat trouvé"

        return render(request, 'resultatRecherche.html', {'text': text, 'artiste' : resultArtiste, 'album' : resultAlbum, 'musique': resultMusique})

    return render(request, template_name='index.html')


def musiquesDetail(request, id):
    if id != None :
        musique = Musique.objects.get(id=id)
    return render(request, template_name='index.html', context={'musique': musique})

def artistesDetail(request, id):
    if id != None :
        artiste = Artiste.objects.get(id=id)
        albums = Album.objects.all().filter(id_artiste=artiste.id).order_by('-date_publication_album')
        musiques = Musique.objects.none()
        for album in albums:
            musiques = musiques | Musique.objects.all().filter(id_album=album.id)
            #musiques = {**musiques, **musiquesTmp}
        return render(request, template_name='artistesDetail.html', context={'artiste': artiste, 'albums': albums, 'musiques': musiques})

def albumsDetail(request, id):
    if id != None :
        album = Album.objects.get(id=id)
        musiques = Musique.objects.all().filter(id_album=album.id)
        extraData = {}
        times = []
        for musique in musiques:
            times.append(musique.duree_musique)
        extraData['totalTime'] = totalDuree(times)
        return render(request, template_name='albumsDetail.html', context={'album': album, 'musiques': musiques, 'extraData': extraData})

def credit(request):
    return render(request, template_name='credit.html')

