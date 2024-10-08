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
from time import sleep
import random
#chnage to request info from my pc

machine_ip = "192.168.0.70"
url = f"http://{machine_ip}:10767/api/v1/playback"



#response = requests.get(url)

client_id = ''
client_secret = ''



def is_cider_active():
    try:
        response = requests.get(url + "/active")
        if response.status_code == 204:
            #print("Cider is active.")
            return True
        else:
            #print(f"Unexpected response: {response.status_code}")
            return False
    except requests.ConnectionError:
        #print("Cider is not active.")
        return False


def get_current_playing_song():
    try:
        response = requests.get(url + "/now-playing")
        if response.status_code == 200:
            song_info = response.json()  # Parse the JSON response
            return song_info["info"]
        else:
            print(f"Unexpected response: {response.status_code}")
            return None
    except requests.ConnectionError:
        #print("Could not connect to Cider.")
        return None

def isSongOn(info):
    try:
        if info["name"] is not None:
            return True
    except:
        return False


print(get_current_playing_song())

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

def getSongInfo():
    if is_cider_active():
        current = get_current_playing_song()
        if isSongOn(current):
            song = current["name"]
            imageURL = current["artwork"]["url"]
            artist = current["artistName"]

            return [song, imageURL, artist]
    else:
        print("cider Is not active")





def SkipSong():
    if is_cider_active():
        requests.post(url + "/next")

def RewindSong():
    if is_cider_active():
        requests.post(url + "/previous")

def Pause_PlaySong():
    if is_cider_active():
        requests.post(url + "/playpause")
  




