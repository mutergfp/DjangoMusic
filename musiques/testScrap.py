# Exercice 4 - Erwan GAY-CHANTELOUP
import requests
from bs4 import BeautifulSoup
import urllib3

# Liste de toutes les licences professionnelles de l'IUT Orleans
parametre = {"submit-form":"",
         "zone-item-id":"zoneItem://c8e50408-29b9-4eb9-9b3f-1c209fb2d75b",
         "catalog":"odf-2018-2022",
         "title":"",
         "textfield":"",
         "degree":"DP",
         "orgUnit":"",
         "place":"45000"}
lp = requests.post("https://formation.univ-orleans.fr/fr/formation/rechercher-une-formation.html#nav", data = parametre)
soup_lp = BeautifulSoup(lp.text, "lxml")
liste_lp = soup_lp.find_all("li", class_="hit")
print("\nListe des licences professionnelles à l'Université d'Orléans : ")
for l in liste_lp:
    print(l.p.strong.text)

# Liste de tout les masters en ecologie
parametre = {"submit-form":"",
         "zone-item-id":"zoneItem://c8e50408-29b9-4eb9-9b3f-1c209fb2d75b",
         "catalog":"odf-2018-2022",
         "title":"",
         "textfield":"écologie",
         "degree":"XB",
         "orgUnit":"",
         "place":""}
mast_eco = requests.post("https://formation.univ-orleans.fr/fr/formation/rechercher-une-formation.html#nav", data = parametre)
soup_mast_eco = BeautifulSoup(mast_eco.text, "lxml")
liste_mast_eco = soup_mast_eco.find_all("li", class_="hit")
print("\nListe des masters en écologie : ")
for l in liste_mast_eco:
    print(l.p.strong.text)

# Liste de toutes les formations de l'IUT Orleans
parametre = {"submit-form":"",
         "zone-item-id":"zoneItem://c8e50408-29b9-4eb9-9b3f-1c209fb2d75b",
         "catalog" : "odf-2018-2022",
         "title":"",
         "textfield":"",
         "degree":"",
         "orgUnit": "orgunitContent://9ee7f4af-c6e8-406a-8292-dea5cdf178c1",
         "place":"45000"}
iut = requests.post("https://formation.univ-orleans.fr/fr/formation/rechercher-une-formation.html#nav", data = parametre)
soup_formations_iut = BeautifulSoup(iut.text, "lxml")
liste_formations = soup_formations_iut.find_all("li", class_="hit")
print("\nListe des formations de l'IUT d'Orléans : ")
for l in liste_formations:
    print(l.p.strong.text)
url = 'https://formation.univ-orleans.fr/fr/formation/rechercher-une-formation.html'
parametre = {'search-degree-6524035014070634' : 'DP', 'search-place-6524035014070634' : '45000'}


