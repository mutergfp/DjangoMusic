from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resultatRecherche/', views.resultatRecherche, name='resultatRecherche'),
    path('albums/<int:id>', views.albumsDetail, name='albumsDetail'),
    path('musiques/<int:id>', views.musiquesDetail, name='musiquesDetail'),
    path('artistes/<int:id>', views.artistesDetail, name='artistesDetail'),
    path('credit', views.credit, name='credit')
]
