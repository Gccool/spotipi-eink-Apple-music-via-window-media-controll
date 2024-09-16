#import logging
#import spotipy
#import spotipy.util as util

import requests
from io import BytesIO
from PIL import Image
import requests
import aiohttp
import asyncio
import base64
#chnage to request info from my pc

machine_ip = "192.168.0.70"
url = f"http://{machine_ip}:5000/main"

#response = requests.get(url)

client_id = 'Client Id'
client_secret = 'Client Secret'


def get_access_token():
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data={"grant_type": "client_credentials"})
    return response.json()['access_token']



def get_thumbnail(access_token, track_name, artist_name, album_name):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    query = f"track:{track_name} artist:{artist_name} album:{album_name}"
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
            if response.status == 200:
                media_info = await response.json()
                token = get_access_token()
                title = media_info['title']
                if split_album_artist_check:
                    artist, album = split_album_artist(media_info['album_artist'])
                else:
                    print('album_artist split error')


                thumb_url = get_thumbnail(token, title, artist, album)

                return [title, thumb_url, artist]

            else:
                print(response.status)
                
#Add suport for the buttons to pause, skip, rewind - https://forums.pimoroni.com/t/inky-impression-7-3-buttons-demo/24457/2 (and possibly rotary                
#encoder to controll apple music volume https://stackoverflow.com/questions/20828752/python-change-master-application-volume)                

#print(asyncio.run(getSongInfo()))
#return [song, imageURL, artist]

#network aint requesting right
