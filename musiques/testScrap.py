import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup
from models import Artiste
getArtiste = Artiste.objects.get(nom_artiste = "Booba")
print(getArtiste.id)