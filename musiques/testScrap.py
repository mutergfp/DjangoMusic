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

def create_musiques():
    import requests
    from bs4 import BeautifulSoup
    html = requests.get("https://www.allformusic.fr/vald/ce-monde-est-cruel").text

    soup = BeautifulSoup(html, 'lxml')
    SongList = soup.findAll('li', itemprop="tracks")
    for song in SongList:
        print(song.strong.text)
        print(song.text[-5:-1])
        break
create_musiques()
