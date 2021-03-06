from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('search/<text>', views.resultSearch, name='resultSearch'),
    path('albums/<int:id>', views.albumsDetail, name='albumsDetail'),
    path('musiques/<int:id>', views.musiquesDetail, name='musiquesDetail'),
    path('artistes/<int:id>', views.artistesDetail, name='artistesDetail'),
    path('credit', views.credit, name='credit'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name="sign_in"),
    path('logout', views.logoutUser, name="logoutUser"),
    path('compte', views.compte, name='compte'),
    path('compte/addPlaylist/', views.addPlaylist, name='addPlaylist'),
    path('compte/playlists/<int:id>', views.listPlaylist, name='listPlaylist'),
    path('compte/deletePlaylist/<int:id>', views.deletePlaylist, name='deletePlaylist'),
    path('compte/editPlaylist/<int:id>', views.editPlaylist, name='editPlaylist'),
    path('compte/playlist/<int:idPlaylist>/<int:idMusique>', views.deletePlaylistMusique, name='deletePlaylistMusique'),
    path('compte/musique/<int:id>/add', views.addPlaylistMusique, name='addPlaylistMusique'),
    path('compte/musique/<int:idPlaylist>/<int:idMusique>', views.computePlaylistMusique, name='computePlaylistMusique')
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
