import spotipy
import numpy as np
import pandas as pd
import time
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2

## Set Up Authentication
token = 'BQDOjopqXmntfZ_pgbrS_MzD6fvnOyi1Sjuvfsu1Fa5G0Kz9hFhce5ZvHr5sj-XsYgcdnBod4k6JMAPBspLcnLZXlhQVyJU_X7lRKPvsi3ma9rB0JtHlLOUNhKc5E9CS7aEhHBf5vK41HClwVVo8SLesL-jHUzUUPU4S1ynLQk94kJ-rQQcMbgBlh5CAyyow_ZV_raJTQLQPGlCzpUyxzFOyqhvTYL3_oQBlU_GkiTW14bzFZEJm-vPqY8SRcEmvHlWSFJfqQpZD1vycQSb-h7a6xQ'
sp = spotipy.Spotify(auth=token)

## Create Empty Dataframes to fill
track_list = []
sorted_list = []
track_df = pd.DataFrame(
    columns=['track', 'artist', 'song', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
             'acousticness',
             'instrumentalness', 'liveness', 'valence', 'tempo'])
start_sort_df = pd.DataFrame(columns=['Track_1', 'Track_2', 'Diff'])


## Get set of liked tracks from spotify API
def get_tracks(response):
    for item in response['items']:
        track = item['track']
        track_list.append(track['id'])


response = sp.current_user_saved_tracks()
get_tracks(response)

while response['next']:
   response = sp.next(response)
   get_tracks(response)

print(track_list)


## Get Track by track data
def get_data(track):
    track_name = sp.track(track)
    track_data = sp.audio_features(track)[0]
    artist = track_name['artists'][0]['name']
    song = track_name['name']
    danceability = track_data['danceability']
    energy = track_data['energy']
    key = track_data['key']
    loudness = track_data['loudness']
    mode = track_data['mode']
    speechiness = track_data['speechiness']
    acousticness = track_data['acousticness']
    instrumentalness = track_data['instrumentalness']
    liveness = track_data['liveness']
    valence = track_data['valence']
    tempo = track_data['tempo']
    track_row = [track, artist, song, danceability, energy, key, loudness, mode, speechiness, acousticness,
                 instrumentalness, liveness, valence, tempo]
    track_df.loc[len(track_df)] = track_row


for track in track_list:
    get_data(track)
print(track_df)

## Update to z score
cols = list(track_df.columns)
cols.remove('track')
cols.remove('song')
cols.remove('artist')
track_df[cols]
for col in cols:
    col_zscore = col + '_zscore'
    track_df[col_zscore] = (track_df[col] - track_df[col].mean()) / track_df[col].std(ddof=0)

print(track_df)


##
def find_distance(track1, track2):
    track_data1 = track_df.loc[
        track_df['track'] == track1, ['danceability_zscore', 'energy_zscore', 'loudness_zscore', 'mode_zscore',
                                      'speechiness_zscore', 'acousticness_zscore',
                                      'instrumentalness_zscore', 'liveness_zscore', 'valence_zscore',
                                      'tempo_zscore']].values[0]
    track_data2 = track_df.loc[
        track_df['track'] == track2, ['danceability_zscore', 'energy_zscore', 'loudness_zscore', 'mode_zscore',
                                      'speechiness_zscore', 'acousticness_zscore',
                                      'instrumentalness_zscore', 'liveness_zscore', 'valence_zscore',
                                      'tempo_zscore']].values[0]
    dist = np.linalg.norm(track_data1 - track_data2)
    return dist


## Set up initial sort to find starting point
tracks_to_sort = track_list.copy()
while tracks_to_sort:
    t1 = tracks_to_sort[0]
    tracks_to_sort.remove(t1)
    for t2 in tracks_to_sort:
        diff = find_distance(t1, t2)
        new_row = [t1, t2, diff]
        start_sort_df.loc[len(start_sort_df)] = new_row

start_sort_df.sort_values(by=['Diff'], ascending=False, inplace=True, ignore_index=True)
start_sort_df.reset_index(drop=True)

current_track = start_sort_df.iloc[0]['Track_1']
print(current_track)

while len(track_list) > 1:
    sorted_list.append(current_track)
    track_list.remove(current_track)
    holding_df = pd.DataFrame(columns=['Track', 'Diff'])
    for track in track_list:
        new_row = [track, find_distance(current_track, track)]
        holding_df.loc[len(holding_df)] = new_row
    holding_df.sort_values(by=['Diff'], ascending=True, inplace=True, ignore_index=True)
    holding_df.reset_index(drop=True)
    current_track = holding_df.iloc[0]['Track']
    print(current_track)

print(track_list[0])

print(sorted_list)


user = ''.join(filter(lambda i: i.isdigit(), sp.current_user()['uri']))

playlist_name = 'Sorted '+ time.strftime( '%d:%m:%Y',time.localtime())

sp.user_playlist_create(user, playlist_name)

playlist = sp.user_playlists(user)

playlist_id = (playlist['items'][0]['id'])

sp.playlist_add_items(playlist_id, sorted_list)

