import requests
import json




def get_account_info():

    api_ID = "b462b99712f64dcb94f3aab35a21827a"
    api_link = "https://accounts.spotify.com/authorize"

    entetes = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(api_ID)}

    api_url = '{0}account'.format(api_link)

    response = requests.get(api_url, headers=entetes)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

print(get_account_info())