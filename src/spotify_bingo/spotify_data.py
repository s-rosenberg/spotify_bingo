import os
from dotenv import load_dotenv

import requests

from typing import List, Dict
import json
from PIL import Image

from constants import ENVFILE, PLAYLIST_DATA_URL, SPOTIFY_TOKEN_URL

def __get_auth_bearer() -> str:
    load_dotenv(ENVFILE)
    
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    request_body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(
        url = SPOTIFY_TOKEN_URL,
        headers = headers,
        data = request_body
    )
    
    access_token_data = response.json()
    return access_token_data.get('access_token')

def __get_headers() -> Dict[str, str]:
    AUTH_BEARER = __get_auth_bearer()
    headers = {
        'Authorization': f'Bearer {AUTH_BEARER}'
    }
    return headers

def get_playlist_data(playlist_id: str) -> List[dict]:
    headers = __get_headers()
    response = requests.get(
        PLAYLIST_DATA_URL.format(playlist_id=playlist_id), 
        headers=headers)
    data = response.json()

    return data.get('items')

def save_image_to_file(image_url:str, filepath: str) -> None:
    response = requests.get(image_url, stream=True).raw
    img = Image.open(response)
    img.save(filepath)

def get_images(song_data: dict) -> List[str]:
    images = list()
    images_from_album = song_data.get('album', {}).get('images', [])
    images += [image.get('url') for image in images_from_album]
    images_from_external_urls = song_data.get('external_urls', {}).get('images', [])
    images += [image.get('url') for image in images_from_external_urls]

    if not any(images):
        raise ValueError(f"Couldn't find images for {get_title(song_data)}")
    return images

def get_title(song_data: dict) -> str:
    return song_data['track']['name'].split('-')[0].strip()

def get_artist(song_data: dict) -> str:
    artists = song_data['track']['artists']
    return ', '.join([artist['name'] for artist in artists])

if __name__ == '__main__':
    print(get_playlist_data('2bkPhR6wORdInvwLZDpD8K'))