import pandas as pd
import spotipy
from Spotify.Modules import send_to_sql


def get_track_data_single(track, token):
    sp = spotipy.Spotify(auth=token)
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
    return track_row


def get_track_data(track_list, token):
    track_df = pd.DataFrame(
        columns=['track', 'artist', 'song', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo'])
    for track in track_list:
        query = "Select * from Track_data where track = \'" + track + "\'"
        print(query)
        response = send_to_sql.recive(query)
        if response:
            query = "Select * from Track_data where track = \'" + track + "\'"
            track_row = send_to_sql.recive(query)
        else:
            track_row = get_track_data_single(track, token)
            query = "insert into Track_data values " + str(tuple(track_row))
            send_to_sql.send(query)
        track_df.loc[len(track_df)] = track_row

    return track_df


def update_to_zscore(track_df):
    cols = list(track_df.columns)
    cols.remove('track')
    cols.remove('song')
    cols.remove('artist')
    track_df[cols]
    for col in cols:
        col_zscore = col + '_zscore'
        track_df[col_zscore] = (track_df[col] - track_df[col].mean()) / track_df[col].std(ddof=0)


def show_metadata_no_requests(track_list, track_df):
    for track in track_list:
        track_data = track_df.loc[
            track_df['track'] == track, ['artist', 'song']].values[0]
        return track_data


def show_metadata(track, token):
    sp = spotipy.Spotify(auth=token)
    track_name = sp.track(track)
    artist = track_name['artists'][0]['name']
    song = track_name['name']
    track_row = [track, artist, song]
    return track_row
