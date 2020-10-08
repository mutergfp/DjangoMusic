from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Artiste, Musique, Album
from django import forms

# Create your views here.
def index(request):
    search_form = Recherche()
    return render(request, 'index.html', {'search': search_form})

"""
class RechercheArtiste(ModelForm):
    class Meta:
        model = Artiste
        fields = ('nom_artiste',)

class RechercheAlbum(ModelForm):
    class Meta:
        model = Album
        fields = ('nom_album',)

class RechercheMusique(ModelForm):
    class Meta:
        model = Musique
        fields = ('titre_musique',)
"""

class Recherche(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Recherche, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    search = forms.CharField(max_length=250)
    
