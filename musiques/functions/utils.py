def totalDuree(strs):
    minutes = 0
    tmpMinutes = 0
    tmpSecondes = 0
    secondes = 0
    for time in strs :
        elements = time.split(':')
        tmpMinutes += int(elements[0], 10)
        tmpSecondes += int(elements[1], 10)
        while tmpSecondes!=0 :
            if (tmpSecondes >= 60) :
                tmpSecondes -= 60
                tmpMinutes += 1
            else :
                secondes = tmpSecondes
                minutes = tmpMinutes
                break
    return "" + str(minutes) + ":" + str(secondes)

def replace_special(texte):
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â', ' ', '\'']
    sans_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a', '-', '-']
    i = 0
    while i < len(accent):
        texte = texte.replace(accent[i], sans_accent[i])
        i += 1
    return texte

def scrap_desc_artiste(artiste):
    import requests
    from bs4 import BeautifulSoup
    from musiques.models import Artiste
    html = requests.get("https://www.allformusic.fr/"+replace_special(artiste.lower())).text

    soup = BeautifulSoup(html, 'lxml')

    ArtisteDescription = soup.find('div', class_ = "read")
    if(ArtisteDescription == None or ArtisteDescription.text == "La page que vous demandez n'existe pas."):
        return "Pas de description disponnible pour cet artiste"
    else:
        return ArtisteDescription.text

def spotify_create_artiste(name_artiste):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    from musiques.models import Artiste
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    artistes = sp.search(q="artist:"+name_artiste, type="artist")
    i = 0
    for artiste in artistes['artists']['items']:
        try:
            getArtiste = Artiste.objects.get(nom_artiste=artiste['name'])
        except Artiste.DoesNotExist:
            if not artistes['artists']['items'][i]['images']:
                A = create_one_artiste(artiste['name'], artiste['id'], scrap_desc_artiste(artiste['name']))
            else:
                A = create_one_artiste(artiste['name'], artiste['id'], scrap_desc_artiste(artiste['name']), artistes['artists']['items'][i]['images'][0]['url'])
            create_one_recherche(artiste['name'])
        i+=1 

def create_one_artiste(nom, id_spotify, description=None, image=None):
    from musiques.models import Artiste, Album, Musique
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    if(image == None):
        A = Artiste(nom_artiste=nom, description_artiste=description, spotify_id_artiste=id_spotify)
    elif(description == None): 
        A = Artiste(nom_artiste=nom, image_artiste=image, spotify_id_artiste=id_spotify)
    elif(description == None and image == None):
        A = Artiste(nom_artiste=nom, spotify_id_artiste=id_spotify)
    else:
        A = Artiste(nom_artiste=nom, description_artiste=description, image_artiste=image, spotify_id_artiste=id_spotify)
    A.save()
    artiste = Artiste.objects.get(nom_artiste=nom, spotify_id_artiste=id_spotify)
    create_artist_albums(artiste)
    # nous devons maintenant importer toutes ses musiques à partir d'ici et nul part autre !!!!!!

def create_one_album(nom, type, image, date, artiste, id_spotify, genre, lien):
    from musiques.models import Album, Artiste
    A, created = Album.objects.get_or_create(nom_album=nom, type_album=type, image_album=image, date_publication_album=date, id_artiste=artiste, spotify_id_album=id_spotify, id_genre=genre, lien_album=lien)
    create_musiques(A)

def create_one_recherche(contenu):
    from musiques.models import Recherche
    r = Recherche(contenu_recherche=contenu)
    r.save()

def create_one_musique(album, titre, duree):
    from musiques.models import Artiste, Musique, Album
    M, created = Musique.objects.get_or_create(titre_musique=titre, duree_musique=duree, id_album=album)
    M.id_artiste.add(album.id_artiste)

def create_artist_albums(artiste):
    import requests
    from bs4 import BeautifulSoup
    html = requests.get("https://www.allformusic.fr/"+replace_special(artiste.nom_artiste.lower())+"/discographie").text

    soup = BeautifulSoup(html, 'lxml')

    AlbumSearch = soup.find('article', id = "disco-album")
    if AlbumSearch:
        for albums in AlbumSearch.ol:
            date_sortie = albums.span.text
            create_one_album(albums.strong.text, "Album", albums.img['data-src'], albums.span.text, artiste, "0", get_or_create_genre(albums.strong.text, artiste.nom_artiste), albums.a['href'])

def combine_genre(genres):
    final = ""
    for i in range(len(genres)):
        if(i == len(genres)-1 and len(genres) > 1):
            final = final[0:len(final)-2]
            final += " et "+genres[i]
        else:
            final += genres[i]+", "
    if(final == ""):
        final = "Aucun"
    return final

def get_or_create_genre(nAlbum, nArtiste):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    from musiques.models import Artiste, Genre
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    artistes = sp.search(q="artist:"+nArtiste, type="artist")
    for a in artistes['artists']['items']:
        if(a['name'] == nArtiste):
            genres = a['genres']
    if not genres:
        genre = combine_genre("")
    else:
        genre = combine_genre(genres)
    G, created = Genre.objects.get_or_create(nom_genre=genre, description_genre=genre)
    return G

def create_musiques(album):
    import requests
    from bs4 import BeautifulSoup
    html = requests.get("https://www.allformusic.fr/"+album.lien_album).text

    soup = BeautifulSoup(html, 'lxml')
    SongList = soup.findAll('li', itemprop="tracks")
    for song in SongList:
        create_one_musique(album, song.strong.text, song.text[-5:-1])
   
    
