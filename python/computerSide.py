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

import requests





async def get_media_info():
    sessions = await mediaManager.request_async()
    
    
    current_session = sessions.get_current_session()
    current_session.source_app_user_model_id

    if current_session:
        
        if current_session.source_app_user_model_id == "AppleInc.AppleMusicWin_nzyj5cx40ttqa!App":

            info = await current_session.try_get_media_properties_async()

            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

            info_dict['genres'] = list(info_dict['genres'])

            breakpoint()

            return info_dict
    
    








def main():
    #requests.
    current_media_info = get_media_info()
    if current_media_info != None:
        Title = current_media_info['title']
        Album_Artist =  current_media_info['album_artist']
        return Title, Album_Artist
    
            
            
            
main()