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
from flask import Flask, jsonify, request
from quart import Quart, jsonify


app = Quart(__name__)


async def get_media_info():
    sessions = await mediaManager.request_async()
    
    
    current_session = sessions.get_sessions()

    for ses in current_session:
        if ses.source_app_user_model_id == "AppleInc.AppleMusicWin_nzyj5cx40ttqa!App":
            current_session = ses
            break

    

    #breakpoint()

    if current_session:
        if current_session.source_app_user_model_id == "AppleInc.AppleMusicWin_nzyj5cx40ttqa!App":
            if await current_session.try_get_media_properties_async() is not None:

                info = await current_session.try_get_media_properties_async()

                info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

                info_dict['genres'] = list(info_dict['genres'])

                #breakpoint()

                return info_dict
    
    
    







@app.route('/main', methods=['GET'])
async def main():
    #requests.
    current_media_info = await get_media_info()
    #breakpoint()
    if current_media_info is not None:
        Title = current_media_info['title']
        Album_Artist =  current_media_info['album_artist']
        return jsonify({'title': Title, 'album_artist': Album_Artist})
    else:
        return jsonify({'error': 'No media information available'}), 404
            
            
            
            
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)