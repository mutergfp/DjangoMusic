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

def spotify_create_artiste(name_artiste):
    cid ="b462b99712f64dcb94f3aab35a21827a"
    secret="cf75ea5330b44a8d8024d8ecc31c8b52"

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager
    =
    client_credentials_manager)

    artistes = sp.search(q="artist:"+name_artiste, type="artist")
    tab = []
    img = []
    desc = []

    i = 0

    for artiste in artistes['artists']['items']:
        img.append(artiste['images'])
        print(img[i][0]['url'])
        i+=0


    # for i in range(10):
                    
    #     desc.append(scrap_desc_artiste(tab[i]))
    #     print()
    #     A.save()
    #     r = Recherche(contenu_recherche=tab[i], compteur_recherche=1)
    #     r.save()

spotify_create_artiste("Vald")