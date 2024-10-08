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





def is_cider_active():
    try:
        response = requests.get(url + "/active")
        if response.status_code == 200:
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
        response = requests.post(url + "/next")
        if response.status_code == 200:
            print("Skipped to the next track successfully.")
        else:
            print(f"Failed to skip track: {response.status_code} - {response.text}")

def RewindSong():
    if is_cider_active():
        response = requests.post(url + "/previous")
        if response.status_code == 200:
            print("Skipped to the next track successfully.")
        else:
            print(f"Failed to skip track: {response.status_code} - {response.text}")

def Pause_PlaySong():
    if is_cider_active():
        response = requests.post(url + "/playpause")
        if response.status_code == 200:
            print("Skipped to the next track successfully.")
        else:
            print(f"Failed to skip track: {response.status_code} - {response.text}")



