import requests
import json
from typing import List

with open('credentials.json') as file:
    headers_data = json.load(file)

headers = {'Authorization': f'Bearer {headers_data["access_token"]}'}

URL = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
PLAYLIST_ID = "2bkPhR6wORdInvwLZDpD8K"
response = requests.get(URL.format(playlist_id=PLAYLIST_ID), headers= headers)

data = response.json()
data = data['items']

def get_images(data: dict) -> List[str]:
    try:
        images = list()
        from_album = data.get('album',{}).get('images',[])
        images += [image['url'] for image in from_album]
        from_external_urls = data.get('external_urls',{}).get('images',[])
        images += [image['url'] for image in from_external_urls]
        # from_artist = data.get('artists',{}).get('images',[])
        return images
    except Exception as ex:
        print(ex)
        print(data)
        input('')
resumed_data = list()

for item in data:
    item = item['track']
    payload = {
        'title': item['name'].split('-')[0].strip(),
        'image': get_images(item)[0],
        'artist': ', '.join([artist['name'] for artist in item['artists']])
    }
    resumed_data.append(payload)

with open('data_spotify.json', 'w') as file:
    json.dump(resumed_data, file, indent=4, ensure_ascii=False)