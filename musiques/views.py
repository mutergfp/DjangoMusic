from django.shortcuts import render, redirect
from django.http import HttpResponse
#from task.models import Album, Musique, Artiste, Label
from django.forms import ModelForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, template_name='index.html')