from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Artiste, Musique, Album
from django import forms

# Create your views here.

class Recherche(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Recherche, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    search = forms.CharField(max_length=250)

def index(request):
    if(request.method == "POST"):
        form = Recherche(request.POST)
        if(form.is_valid()):
            return redirect('search/'+request.POST['search'])
    else:
        search_form = Recherche()
        return render(request, 'index.html', {'search': search_form})

def resultSearch(request, text=None):
    if(text != None):
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

    
