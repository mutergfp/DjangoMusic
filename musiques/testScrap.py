import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup

def scrap_desc_artiste(artiste):

    

    html = requests.get("https://www.allformusic.fr/"+artiste.lower()).text

    soup = BeautifulSoup(html, 'lxml')

    ArtisteDescription = soup.find('div', class_ = "read")
    if(ArtisteDescription == None):
        return "Pas de description disponnible pour cet artiste"
    else:
        return ArtisteDescription.text

cid ="b462b99712f64dcb94f3aab35a21827a"
secret="cf75ea5330b44a8d8024d8ecc31c8b52"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)

name="Booba"

artistes = sp.search(q="artist:"+name, type="artist")
tab = []

for artiste in artistes['artists']['items']:
    tab.append(artiste['name'])

desc = []

for i in range(len(tab)):
    desc.append(scrap_desc_artiste(tab[i]))

