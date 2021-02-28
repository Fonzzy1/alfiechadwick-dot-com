import pandas as pd
import spotipy

track_list = pd.DataFrame(columns=['track'])


def get_liked_tracks_subset(response):
    for item in response['items']:
        track = item['track']['id']
        track_list.loc[len(track_list)] = track


def get_liked_tracks(token):
    sp = spotipy.Spotify(auth=token)
    response = sp.current_user_saved_tracks()
    get_liked_tracks_subset(response)
    while response['next']:
        response = sp.next(response)
        get_liked_tracks_subset(response)

    return track_list


def get_top_song_short(token):
    sp = spotipy.Spotify(auth=token)
    item = sp.current_user_top_tracks(1, 0, 'short_term')
    track = item['items'][0]['id']
    return track


def get_top_song_medium(token):
    sp = spotipy.Spotify(auth=token)
    item = sp.current_user_top_tracks(1, 0, medium_term)
    track = item['items'][0]['id']
    return track


def get_top_song_long(token):
    sp = spotipy.Spotify(auth=token)
    item = sp.current_user_top_tracks(1, 0, long_term)
    track = item['items'][0]['id']
    return track
