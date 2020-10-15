import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup

def scrap_desc_artiste(artiste):
 
    html = requests.get("https://www.allformusic.fr/"+replace_special(artiste.lower())).text

    soup = BeautifulSoup(html, 'lxml')

    ArtisteDescription = soup.find('div', class_ = "read")
    if(ArtisteDescription == None):
        return "Pas de description disponnible pour cet artiste"
    else:
        return ArtisteDescription.text

def replace_special(texte):
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â', ' ', '\'']
    sans_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a', '-', '-']
    i = 0
    while i < len(accent):
        texte = texte.replace(accent[i], sans_accent[i])
        i += 1
    return texte

def spotify_create_album(name_album):
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager
    =
    client_credentials_manager)

    albums = sp.search(q="album:"+name_album, type="album")
    
    for album in albums['albums']['items']:
        print(album['artists'][0]['name']+" : "+album['name']+". Image : "+album['images'][0]['url']+". Type : "+album['album_type']+". Date de parution : "+album['release_date'])

    print(albums['albums']['items'][0])  

    # for artiste in albums['artists']['items']:
    #     print(artiste)
    #     print('\n')

spotify_create_album("Dans la légende")