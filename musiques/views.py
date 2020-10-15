from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Artiste, Musique, Album, Recherche
from django import forms
from musiques.functions.utils import totalDuree
import requests
from bs4 import BeautifulSoup

# Create your views here.

class RechercheForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RechercheForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Artiste / Albums / Musique'

    search = forms.CharField(max_length=250)

def traitementRecherche(request):
    if(request.method == "POST"):
        form = RechercheForm(request.POST)
        if(form.is_valid()):
            return redirect('/search/'+request.POST['search'])
    else:
        return RechercheForm()


def index(request):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        return render(request, 'index.html', {'search': search_form})

def resultSearch(request, text=None):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if(text != None):
            try: 
                issetRecherche = Recherche.objects.get(contenu_recherche = text)
            except Recherche.DoesNotExist:
                r = Recherche(contenu_recherche=text, compteur_recherche=1)
                r.save()
            else:
                issetRecherche.compteur_recherche += 1
                issetRecherche.save()

            try:
                resultArtiste = Artiste.objects.get(nom_artiste = text)
            except Artiste.DoesNotExist:
                resultArtiste = "Aucun résultat trouvé"
            
            try:
                resultAlbum = Album.objects.get(nom_album = text)
            except Album.DoesNotExist:
                resultAlbum = "Aucun résultat trouvé"
            
            try:
                resultMusique = Musique.objects.get(titre_musique = text)
            except Musique.DoesNotExist:
                resultMusique = "Aucun résultat trouvé"

            return render(request, 'resultatRecherche.html', {'search': search_form, 'text': text, 'artiste' : resultArtiste, 'album' : resultAlbum, 'musique': resultMusique})
        return render(request, template_name='index.html')


def musiquesDetail(request, id):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if id != None :
            musique = Musique.objects.get(id=id)
        return render(request, template_name='index.html', context={'search': search_form, 'musique': musique})

def artistesDetail(request, id):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if id != None :
            artiste = Artiste.objects.get(id=id)
            albums = Album.objects.all().filter(id_artiste=artiste.id).order_by('-date_publication_album')
            musiques = Musique.objects.none()
            for album in albums:
                musiques = musiques | Musique.objects.all().filter(id_album=album.id)
                #musiques = {**musiques, **musiquesTmp}
            return render(request, template_name='artistesDetail.html', context={'search': search_form, 'artiste': artiste, 'albums': albums, 'musiques': musiques})

def albumsDetail(request, id):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if id != None :
            album = Album.objects.get(id=id)
            musiques = Musique.objects.all().filter(id_album=album.id)
            extraData = {}
            times = []
            for musique in musiques:
                times.append(musique.duree_musique)
            extraData['totalTime'] = totalDuree(times)
            return render(request, template_name='albumsDetail.html', context={'search': search_form, 'album': album, 'musiques': musiques, 'extraData': extraData})

def credit(request):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        return render(request, template_name='credit.html', context={'search': search_form})

def scrap_desc_artiste(artiste):
    html = requests.get("https://www.allformusic.fr/.{artiste}"+format(artiste)).text

    soup = BeautifulSoup(html, 'lxml')

    ArtisteDescription = soup.find('div', class_ = "read")
    return ArtisteDescription.text

