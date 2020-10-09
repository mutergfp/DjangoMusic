from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Album, Artiste, Genre, Label, Musique
import requests

# Create your views here.
def index(request):
    return render(request, template_name='index.html')

def resultatRecherche(request):
    return render(request, template_name='index.html')

def musiquesDetail(request, id):
    if id != None :
        musique = Musique.objects.get(id=id)
    return render(request, template_name='index.html', context={'musique': musique})

def artistesDetail(request, id):
    if id != None :
        artiste = Artiste.objects.get(id=id)
    return render(request, template_name='index.html', context={'artiste': artiste})

def albumsDetail(request, id):
    if id != None :
        album = Album.objects.get(id=id)
    return render(request, template_name='index.html', context={'album': album})

def credit(request):
    return render(request, template_name='index.html')
