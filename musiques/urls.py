from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/?str={str}', views.resultRecherche, name='resultRecherche'),
    path('albums/{id}', views.albumsDetail, name='albumsDetail'),
    path('musiques/{id}', views.musiquesDetail, name='musiquesDetail'),
    path('artistes/{id}', views.artistesDetail, name='artistesDetail'),
    path('credit', views.credit, name='credit')
]
