from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Album, Artiste, Genre, Label, Musique
import requests
from musiques.functions.utils import totalDuree

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
        return render(request, template_name='artistesDetail.html', context={'artiste': artiste})

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
