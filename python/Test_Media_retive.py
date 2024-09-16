import asyncio
from time import sleep
import PIL
from PIL import Image

import requests
import base64
import os
from io import BytesIO

import PIL.Image
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as mediaManager

from winsdk.windows.storage.streams import DataReader, Buffer, InputStreamOptions

import winsdk.windows.media.control as wmc

import cv2


client_id = '88fedb232e9a472b85693ccc983826de'
client_secret = '5a0bc8dd1bf946db9c17fc51c6a9a896'
path = r'C:\Users\GC\Documents\Diy projects\media control\cover.jpg'
previousSong = ''



async def get_media_info():
    sessions = await mediaManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:
        

        info = await current_session.try_get_media_properties_async()

        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        info_dict['genres'] = list(info_dict['genres'])

        return info_dict
    
    


def get_access_token():
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data={"grant_type": "client_credentials"})
    return response.json()['access_token']

# Search for the track
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


def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")

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
    
def delete_file_if_exists(file_path):
    # Check if the file exists
    if os.path.isfile(file_path):
        # Delete the file
        os.remove(file_path)
        #print(f"File '{file_path}' has been deleted.")
    #else:
        #print(f"File '{file_path}' does not exist.")    






def main(previousSong):
    

    current_media_info = asyncio.run(get_media_info())

    

    if current_media_info != None:
        #print(current_media_info)

        token = get_access_token()
        if split_album_artist_check(current_media_info['album_artist']):

            artist, album = split_album_artist(current_media_info['album_artist'])

            title = current_media_info['title']

            currentSong = artist+album+title

            #print(previousSong + '|' + currentSong)

            if previousSong != currentSong:
                previousSong = currentSong
                
            
                delete_file_if_exists(path)



                thumb_url = get_thumbnail(token, title, artist)

                #print(title + artist)

                #print(thumb_url) 

                download_image(thumb_url, path)

                cover = cv2.imread(path)

                cover = cv2.resize(cover, (960, 960))

                cv2.imshow('cover', cover)
                cv2.waitKey(1)

                return previousSong
            else:
                return previousSong

    else:
        cv2.destroyAllWindows()
            
            
            


while True:
    previousSong = main(previousSong)
    sleep(1)


# CHANGE IT TO ONLY PICK UP APPLE MUSIC https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python