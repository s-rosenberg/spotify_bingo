import os
from dotenv import load_dotenv

import requests

from typing import List, Dict
import json

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
    pass

def get_images(song_data: dict) -> List[str]:
    pass

if __name__ == '__main__':
    print(get_playlist_data('2bkPhR6wORdInvwLZDpD8K'))