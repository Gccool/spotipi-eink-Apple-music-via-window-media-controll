import logging
#import spotipy
#import spotipy.util as util

import requests
from io import BytesIO
from PIL import Image
import requests
import aiohttp
import asyncio
#chnage to request info from my pc

machine_ip = "192.168.0.70"
url = f"http://{machine_ip}:5000/main"

#response = requests.get(url)


def get_thumbnail(access_token, track_name, artist_name):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    query = f"track:{track_name} artist:{artist_name}"
    response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track", headers=headers)
    tracks = response.json()['tracks']['items']
    if tracks:
        return tracks[0]['album']['images'][0]['url']
    return None

def split_album_artist(album_artist):
    # Split the string at ' - '
    parts = album_artist.split(' — ')
    if len(parts) == 2:
        album, artist = parts
        return album, artist
    else:
        raise ValueError("The input string must be in the format 'album - artist'")
        
def split_album_artist_check(album_artist):
    # Split the string at ' - '
    parts = album_artist.split(' — ')
    if len(parts) == 2:
        return True
    else:
        #raise ValueError("The input string must be in the format 'album - artist'")
        return False

async def getSongInfo():
  #breakpoint()
    async with aiohttp.ClientSession() as session:
        async with session.get('http://192.168.0.70:5000/main') as response:
            #breakpoint()
            if response.status_code == 200:
              media_info = response.json()
              print("Media Info:", media_info)
            else:
                print(response.status_code)


asyncio.run(getSongInfo())
#return [song, imageURL, artist]

#network aint requesting right
