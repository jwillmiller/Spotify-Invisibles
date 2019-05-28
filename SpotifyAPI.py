# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:47:43 2019

@author: willm
"""

import spotipy
import spotipy.util as util
import os
from json.decoder import JSONDecodeError
import pandas as pd
import spotifyLocalConfig as lc

# localhost for personal use / development
redirect_url = 'http://localhost:8888/callback/'


#get token
scope = 'user-library-read'

try:
    token = util.prompt_for_user_token(lc.username, scope, 
                                       client_id=lc.SPOTIPY_CLIENT_ID, 
                                       client_secret=lc.SPOTIPY_CLIENT_SECRET, 
                                       redirect_uri=redirect_url)
    
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{lc.username}")
    token = util.prompt_for_user_token(lc.username, scope, 
                                       client_id=lc.SPOTIPY_CLIENT_ID, 
                                       client_secret=lc.SPOTIPY_CLIENT_SECRET, 
                                       redirect_uri=redirect_url)

sp = spotipy.Spotify(auth=token)

# get all songs from user playlists
playlistres = sp.current_user_playlists()

playlistids = []
playlist = playlistres['items']
for play in playlist:
    playlistids.append(play['id'])
    
trackids = []    

for playlistid in playlistids:
    tracksres = sp.user_playlist_tracks(lc.username, playlistid)
    tracklist = tracksres['items']
    for track in tracklist:
        trackids.append(track['track']['id'])
        
# for each track, add to a list of features (trackid: danceability, energy, 
# loudness, speechiness, acousticness, instrumentalness, liveness, valence)
dance = []
energy = []
loud = []
speech = []
acoustic = []
instrument = []
live = []
valence = []

for trackid in trackids:
    response = sp.audio_features(trackid)
    r = response[0]
    dance.append(r['danceability'])
    energy.append(r['energy'])
    loud.append(r['loudness'])
    speech.append(r['speechiness'])
    acoustic.append(r['acousticness'])
    instrument.append(r['instrumentalness'])
    live.append(r['liveness'])
    valence.append(r['valence'])

songdata_df = pd.DataFrame({'id': trackids, 'dance': dance, 'energy': energy, 
                            'loud': loud, 'speech': speech, 
                            'acoustic': acoustic, 'instrument': instrument, 
                            'live': live, 'valence': valence})
    
songdata_df.drop_duplicates(inplace=True)


#get a new token with a new scope so that we can write to playlists
scope = 'playlist-modify-public'
try:
    token = util.prompt_for_user_token(lc.username, scope, 
                                       client_id=lc.SPOTIPY_CLIENT_ID, 
                                       client_secret=lc.SPOTIPY_CLIENT_SECRET, 
                                       redirect_uri=redirect_url)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{lc.username}")
    token = util.prompt_for_user_token(lc.username, scope, 
                                       client_id=lc.SPOTIPY_CLIENT_ID, 
                                       client_secret=lc.SPOTIPY_CLIENT_SECRET, 
                                       redirect_uri=redirect_url)

sp = spotipy.Spotify(auth=token)

songdata_df.set_index('id', inplace=True)

for column in songdata_df.columns:
    # make a 'most' playlist
    playlistresponse = sp.user_playlist_create(lc.username, column, public=True)
    songdata_df.sort_values(by=column, ascending=False, inplace=True)
    mosttracks = []
    for i in range(15):
        mosttracks.append(songdata_df.index[i])
    sp.user_playlist_add_tracks(lc.username, playlistresponse['id'], mosttracks)
    
    # make a 'least' playlist
    playlistresponse = sp.user_playlist_create(lc.username, 'least ' + column, 
                                               public=True)
    songdata_df.sort_values(by=column, ascending=True, inplace=True)
    leasttracks = []
    for i in range(15):
        leasttracks.append(songdata_df.index[i])
        
    sp.user_playlist_add_tracks(lc.username, playlistresponse['id'], leasttracks)
