import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid ="b462b99712f64dcb94f3aab35a21827a"
secret="cf75ea5330b44a8d8024d8ecc31c8b52"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)

name="Booba"

artistes = sp.search(q="artist:"+name, type="artist")

print(artistes['artists']['href'])

for artiste in artistes['artists']['items']:
    print(artiste['name'])