import requests
from bs4 import BeautifulSoup
def replace_special(texte):
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â', ' ', '\'']
    sans_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a', '-', '-']
    i = 0
    while i < len(accent):
        texte = texte.replace(accent[i], sans_accent[i])
        i += 1
    return texte

def scrap_disco(nom_artiste):

    html = requests.get("https://www.allformusic.fr/"+replace_special(nom_artiste.lower())+"/discographie").text

    soup = BeautifulSoup(html, 'lxml')

    AlbumSearch = soup.find('article', id = "disco-album")
    for albums in AlbumSearch.ol:
        create_one_scrap_album(albums.a['href'])

def create_one_scrap_album(lien):
    detailsAlbum = requests.get("https://www.allformusic.fr/"+lien).text
    album = []
    sons = []
    time = []
    soup = BeautifulSoup(detailsAlbum, 'lxml')
    titre = soup.find('span', itemprop="name")
    print(titre.text)
    infos = soup.find('div', class_ = "pochette-300")
    album.append(infos.figure.img['src'])
    infos = soup.find('div', id="infos")
    i = 0
    for info in infos.ul:
        if(i != 1 or i != 4):
            album.append(info.text)
        i+=1
    album = formatage_album(album)    
    musiques = soup.find('ol',class_="songsct")
    for musique in musiques:
        time.append(musique.text[-5:-1])
        chaine = musique.text[18:-6]
        if(ord(chaine[0]) == 160):
            chaine= musique.text[19:-6]
        sons.append(chaine)
    print(time)
    print("\n")

def formatage_album(album):
    newAlbum = []
    newAlbum.append(album[0])
    del album[2]
    del album[-1]
    i = 0
    for case in album:
        if(i == 1):
            newAlbum.append(case[10:len(case)])
        if(i == 2):
            newAlbum.append(case[7:len(case)])
        if(i == 3):
            newAlbum.append(case[14:len(case)])
        i+=1
    return newAlbum
scrap_disco("vald")