from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.forms import ModelForm
from django.contrib import messages
from musiques.models import Artiste, Musique, Album, Recherche, Playlist
from django import forms
from musiques.functions.utils import totalDuree
import requests
from bs4 import BeautifulSoup

#Dépendances utilisateur
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

class RechercheForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RechercheForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Artiste / Albums / Musique'

    search = forms.CharField(max_length=250)

def traitementRecherche(request):
    if(request.method == "POST"):
        form = RechercheForm(request.POST)
        if(form.is_valid()):
            return redirect('/search/'+request.POST['search'])
    
    return RechercheForm()


def index(request):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        return render(request, 'index.html', {'search': search_form, })

def resultSearch(request, text=None):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if(text != None):
            try: 
                issetRecherche = Recherche.objects.get(contenu_recherche = text)
            except Recherche.DoesNotExist:
                r = Recherche(contenu_recherche=text, compteur_recherche=1)
                r.save()
            else:
                issetRecherche.compteur_recherche += 1
                issetRecherche.save()

            try:
                resultArtiste = Artiste.objects.get(nom_artiste = text)
            except Artiste.DoesNotExist:
                resultArtiste = "Aucun résultat trouvé"
            
            try:
                resultAlbum = Album.objects.get(nom_album = text)
            except Album.DoesNotExist:
                resultAlbum = "Aucun résultat trouvé"
            
            try:
                resultMusique = Musique.objects.get(titre_musique = text)
            except Musique.DoesNotExist:
                resultMusique = "Aucun résultat trouvé"

            return render(request, 'resultatRecherche.html', {'search': search_form, 'text': text, 'artiste' : resultArtiste, 'album' : resultAlbum, 'musique': resultMusique})
        return render(request, template_name='index.html')


def musiquesDetail(request, id):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if id != None :
            musique = Musique.objects.get(id=id)
        return render(request, template_name='index.html', context={'search': search_form, 'musique': musique})

def artistesDetail(request, id):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if id != None :
            artiste = Artiste.objects.get(id=id)
            albums = Album.objects.all().filter(id_artiste=artiste.id).order_by('-date_publication_album')
            musiques = Musique.objects.none()
            for album in albums:
                musiques = musiques | Musique.objects.all().filter(id_album=album.id)
                #musiques = {**musiques, **musiquesTmp}
            return render(request, template_name='artistesDetail.html', context={'search': search_form, 'artiste': artiste, 'albums': albums, 'musiques': musiques})

def albumsDetail(request, id):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if id != None :
            album = Album.objects.get(id=id)
            musiques = Musique.objects.all().filter(id_album=album.id)
            extraData = {}
            times = []
            for musique in musiques:
                times.append(musique.duree_musique)
            extraData['totalTime'] = totalDuree(times)
            return render(request, template_name='albumsDetail.html', context={'search': search_form, 'album': album, 'musiques': musiques, 'extraData': extraData})

def credit(request):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        return render(request, template_name='credit.html', context={'search': search_form})

def scrap_desc_artiste(artiste):
    html = requests.get("https://www.allformusic.fr/.{artiste}"+format(artiste)).text

    soup = BeautifulSoup(html, 'lxml')

    ArtisteDescription = soup.find('div', class_ = "read")
    return ArtisteDescription.text


####### Utilisateur #######

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Nom de compte"
        self.fields['password'].widget.attrs['placeholder'] = "Mot de passe"
        for visible in self.visible_fields():
            visible.label= ""
            visible.field.widget.attrs['class'] = 'form-control mb-3'

    def confirm_login_allowed(self, user):
        pass

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Nom de compte"
        self.fields['password1'].widget.attrs['placeholder'] = "Mot de passe"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirmation du mot de passe"
        self.fields['username'].help_text = " "
        self.fields['password1'].help_text = "<ul><li>Votre mot de passe ne doit pas être une information personnelle</li><li>Votre mot de passe doit contenir 8 caractères minimum</li><li>Votre mot de passe ne peut pas être des chiffres seulement</li></ul>"
        self.fields['password2'].help_text = "Entrez le même mot de passe que le précédent"
        for visible in self.visible_fields():
            visible.label= ""
            visible.field.widget.attrs['class'] = 'form-control'
#Connexion

def sign_up(request):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if (request.method == "POST"):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Compte connecté")
                return render(request, 'index.html', {'search': search_form })
    form = LoginForm()
    return render(request, template_name='sign_up.html', context={'formLog': form, 'search': search_form})

#Insciption   
def sign_in(request):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Compte enregistré")
                return redirect('/')
        else:
            form = RegisterForm()
            return render(request, template_name='sign_in.html', context={'formLog': form, 'search': search_form})

@login_required
def compte(request):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        user = request.user
        playlists=Playlist.objects.all().filter(id_user=user.id)
        return render(request, template_name='compte.html', context={'search' : search_form, 'playlists' : playlists})

def getUser(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    return user
    
def logoutUser(request):
    logout(request)
    return redirect('/')

####### CRUD Playlist #######

class PlaylistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlaylistForm, self).__init__(*args, **kwargs)
        self.fields['nom_playlist'].widget.attrs['placeholder'] = "Nom de playlist"
        self.fields['nom_playlist'].widget.attrs['class'] = "form-control mb-3"
        self.fields['image_playlist'].widget.attrs['class'] = "form-control"
        
        self.fields['image_playlist'].widget.attrs['accept'] = "image/*"
        self.fields['image_playlist'].help_text = "<div style='text-align: center;'><p>Vous n'êtes pas obligé de mettre une image. <br> Si vous n'en mettez pas une image par défaut sera affiché</p></div>"
        for visible in self.visible_fields():
            visible.label= ""


    class Meta:
        model = Playlist
        fields = ('nom_playlist', 'image_playlist')
    

@login_required
def addPlaylist(request):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if request.method == "POST":
            form = PlaylistForm(request.POST)
            if form.is_valid():
                playlist = form.save(commit=False)
                user = request.user
                playlist.id_user = user
                playlist.save()
                messages.success(request ,'Playlist créée')
                return redirect('compte')
    form = PlaylistForm()
    return render(request, template_name='addPlaylist.html', context={'search' : search_form, 'form': form})

@login_required
def listPlaylist(request, id=None):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    if id == None:
        return redirect('index')
    playlist=Playlist.objects.get(id=id)
    musiques=playlist.id_musique.all()
    artistes=[]
    for musique in musiques:
        album = Album.objects.get(id=musique.id_album.id)
        artistes.append(Artiste.objects.get(id=album.id_artiste.id))
    return render(request, template_name='listPlaylist.html', context={'search' : search_form, 'playlist': playlist, 'musiques': musiques, 'artistes': artistes})

@login_required
def deletePlaylist(request, id=None):
    if id != None:
        if(Playlist.objects.get(id=id)):
            Playlist.objects.get(id=id).delete()
    return redirect('compte')
        
@login_required
def editPlaylist(request, id=None):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if id == None:
            return redirect('compte')
        else:
            playlist = Playlist.objects.get(id=id)
            if request.method == "POST":
                form = PlaylistForm(request.POST, instance=playlist)
                if form.is_valid():
                    playlist = form.save()
                    messages.success(request ,'Playlist modifié')
                    return redirect('compte')
            form = PlaylistForm(instance=playlist)
            return render(request, template_name='editPlaylist.html', context={'search' : search_form, 'form': form})
    return redirect('compte')

@login_required
def deletePlaylistMusique(request, idPlaylist=None, idMusique=None):
    if idPlaylist != None:
        if idMusique != None:
            musique = Musique.objects.get(id=idMusique)
            Playlist.objects.get(id=idPlaylist).id_musique.remove(musique)
            return redirect('listPlaylist', id=idPlaylist)
    return redirect('compte')

@login_required
def addPlaylistMusique(request, id=None):
    search_form = traitementRecherche(request)
    if not isinstance(search_form, RechercheForm):
        return search_form
    else:
        if id != None:
            user = request.user
            playlists = Playlist.objects.all().filter(id_user=user.id)
            musique = Musique.objects.get(id=id)
            return render(request, template_name='addPlaylistMusique.html', context={'search' : search_form, 'playlists': playlists, 'musique': musique})
    return redirect('index')

@login_required
def computePlaylistMusique(request, idPlaylist=None, idMusique=None):
    if idPlaylist != None:
        if idMusique != None:
            playlist = Playlist.objects.get(id=idPlaylist)
            musique = Musique.objects.get(id=idMusique)
            playlist.id_musique.add(musique)
            return redirect('albumsDetail', id=musique.id_album.id)
    return redirect('index')