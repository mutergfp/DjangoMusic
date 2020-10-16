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

@login_required(login_url='/sign_up')
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