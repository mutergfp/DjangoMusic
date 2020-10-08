from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, template_name='index.html')

def resultRecherche(request):
    return render(request, template_name='index.html')

def musiquesDetail(request, id):
    return render(request, template_name='index.html')

def artistesDetail(request, id):
    return render(request, template_name='index.html')

def albumsDetail(request, id):
    return render(request, template_name='index.html')

def credit(request):
    return render(request, template_name='index.html')
