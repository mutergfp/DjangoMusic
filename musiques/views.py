from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Artiste, Musique, Album, Recherche
from django import forms

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

        return render(request, 'resultatRecherche.html', {'text': text, 'artiste' : resultArtiste, 'album' : resultAlbum, 'musique': resultMusique})

def scrap_desc_artiste(artiste):
    html = requests.get("https://www.allformusic.fr/.{artiste}"+format(artiste)).text

    soup = BeautifulSoup(html, 'lxml')

    ArtisteDescription = soup.find('div', class_ = "read")
    return ArtisteDescription.text

