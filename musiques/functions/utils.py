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
    from musiques.models import Artiste
    if(image == None):
        A = Artiste(nom_artiste=nom, description_artiste=description, spotify_id_artiste=id_spotify)
    elif(description == None): 
        A = Artiste(nom_artiste=nom, image_artiste=image, spotify_id_artiste=id_spotify)
    elif(description == None and image == None):
        A = Artiste(nom_artiste=nom, spotify_id_artiste=id_spotify)
    else:
        A = Artiste(nom_artiste=nom, description_artiste=description, image_artiste=image, spotify_id_artiste=id_spotify)
    A.save()

def create_one_recherche(contenu):
    from musiques.models import Recherche
    r = Recherche(contenu_recherche=contenu)
    r.save()

def spotify_create_album(nom_album):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    from musiques.models import Album
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    albums = sp.search(q="album:"+nom_album, type="album")
    
    for album in albums['albums']['items']:
        try:
            issetAlbum = Album.objects.get(nom_album=nom_album)
        except Album.DoesNotExist:
            create_one_album(album['name'], album['artists'][0]['name'])
        
def create_one_album(nom_album, nom_art):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    from musiques.models import Album, Artiste, Genre
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    genreA = ""
    albums = sp.search(q="album:"+nom_album, type="album")
    for album in albums['albums']['items']:        
        if(album['artists'][0]['name'] == nom_art):
            genreA = getGenre(album['name'], nom_art)
            nomA = album['name']
            spotify_idA = album['id']
            if not album['images'][0]['url']:
                imageA = None
            else:
                imageA = album['images'][0]['url']
            if not album['release_date']:
                dateA = None
            else:
                dateA = album['release_date']
            try:
                issetGenre = Genre.objects.get(nom_genre=combine_genre(genreA))
            except Genre.DoesNotExist:
                G = Genre(nom_genre=combine_genre(genreA), description_genre=combine_genre(genreA))
                G.save()
            typeA = album['type']
            idArtiste = Artiste.objects.get(nom_artiste=nom_art)
            createAlbum = Album.objects.get_or_create(nom_album=nomA, type_album=album['type'], image_album=imageA, date_publication_album=dateA, id_artiste=Artiste.objects.get(nom_artiste=nom_art), spotify_id_album=spotify_idA, id_genre=Genre.objects.get(nom_genre=combine_genre(genreA)))

def combine_genre(genres):
    final = ""
    for i in range(len(genres)):
        if(i == len(genres)-1):
            final = final[0:len(final)-2]
            final += " et "+genres[i]
        else:
            final += genres[i]+", "
    if(final == ""):
        final = "Aucun"
    return final

def getGenre(nAlbum, nArtiste):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    from musiques.models import Artiste
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    try:
        artiste = Artiste.objects.get(nom_artiste=nArtiste)
    except Artiste.DoesNotExist:
        artistes = sp.search(q="artist:"+nArtiste, type="artist")
        for a in artistes['artists']['items']:
            if(a['name'] == nArtiste):
                create_one_artiste(a['name'], a['id'], scrap_desc_artiste(a['name']), a['images'][0]['url'])
                create_one_recherche(a['name'])
                return a['genres']
    artistes = sp.search(q="artist:"+nArtiste, type="artist")
    for a in artistes['artists']['items']:
        if(a['name'] == nArtiste):
            return a['genres']
    return ""