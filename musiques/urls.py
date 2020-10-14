from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('resultatRecherche/', views.resultatRecherche, name='resultatRecherche'),
    path('albums/<int:id>', views.albumsDetail, name='albumsDetail'),
    path('musiques/<int:id>', views.musiquesDetail, name='musiquesDetail'),
    path('artistes/<int:id>', views.artistesDetail, name='artistesDetail'),
    path('credit', views.credit, name='credit')
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
