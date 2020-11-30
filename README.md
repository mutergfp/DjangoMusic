# DjangoMusic

## Télécharger le projet

Par ligne de commande : `git clone https://github.com/mutergfp/DjangoMusic.git`

Par téléchargement du dossier .zip : Décompressez le dossier zippé

## Mise en place du projet

1. Dans un terminal, se positionner dans à la racine du projet
2. Entrez `source ~/venv3/bin/activate`
3. Télécharger les modules suivant :
  - Spotipy : `pip install spotipy`
  - BeautifulSoup : `pip install beautifulsoup4`
  - lxml : `pip install lxml`
4. Installez les dépendances avec `yarn install`
5. Importez la base de données `./manage.py migrate`
6. Démarrez le serveur avec `./manage.py runserver`
7. Connectez-vous à l'url `localhost:8000/`

## Pour l'administrateur

1. Créez un superutilisateur avec `./manage.py createsuperuser`
2. Assurez-vous de créer des `users` depuis le panel administrateur pour l'utilisateur du site

## Liste des routes de bases

Pour l'administrateur : `localhost:8000/admin/`

Pour un utilisateur : `localhost:8000/`



