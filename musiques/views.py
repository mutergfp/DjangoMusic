from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Artiste, Musique, Album, Recherche
from django import forms
from musiques.functions.utils import totalDuree
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

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

        resultAlbum = "Aucun résultat trouvé"
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

def replace_special(texte):
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â', ' ', '\'']
    sans_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a', '-', '-']
    i = 0
    while i < len(accent):
        texte = texte.replace(accent[i], sans_accent[i])
        i += 1
    return texte

def scrap_desc_artiste(artiste):
 
    html = requests.get("https://www.allformusic.fr/"+replace_special(artiste.lower())).text

    soup = BeautifulSoup(html, 'lxml')

    ArtisteDescription = soup.find('div', class_ = "read")
    if(ArtisteDescription == None or ArtisteDescription.text == "La page que vous demandez n'existe pas."):
        return "Pas de description disponnible pour cet artiste"
    else:
        return ArtisteDescription.text


def spotify_create_artiste(name_artiste):
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    artistes = sp.search(q="artist:"+name_artiste, type="artist")
    i = 0
    for artiste in artistes['artists']['items']:
        if not artistes['artists']['items'][i]['images']:
            A = create_one_artiste(artiste['name'], scrap_desc_artiste(artiste['name']))
        else:
            A = create_one_artiste(artiste['name'], scrap_desc_artiste(artiste['name']), artistes['artists']['items'][i]['images'][0]['url'])
        create_one_recherche(artiste['name'])
        i+=1 

def create_one_artiste(nom, description=None, image=None):
    if(image == None):
        A = Artiste(nom_artiste=nom, description_artiste=description)
    elif(description == None): 
        A = Artiste(nom_artiste=nom, image_artiste=image)
    elif(description == None and image == None):
        A = Artiste(nom_artiste=nom)
    else:
        A = Artiste(nom_artiste=nom, description_artiste=description, image_artiste=image)
    A.save()

def create_one_recherche(contenu):
    r = Recherche(contenu_recherche=contenu)
    r.save()

def create_one_album(nom, type, image=None, date=None, artiste):
    if(image == None):
        A = Album(nom_album=nom, type_album=type, date_publication_album=date, id_artiste=artiste)
    elif(date==None):
        A = Album(nom_album=nom, type_album=type, image_album=image, id_artiste=artiste)
    elif(date == None and image == None):
        A = Album(nom_album=nom, type_album=type, id_artiste=artiste)
    else:
        A = Album(nom_album=nom, type_album=type, image_album=image, date_publication_album=date, id_artiste=artiste)
    A.save()


