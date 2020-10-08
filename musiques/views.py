from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Artiste, Musique, Album
from django import forms

# Create your views here.
def index(request):

    if(request.method == "POST"):
        form = Recherche(request.POST)
        if(form.is_valid()):
            return render(request, 'resultatRecherche.html')

    search_form = Recherche()
    return render(request, 'index.html', {'search': search_form})

class Recherche(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Recherche, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    search = forms.CharField(max_length=250)
    
