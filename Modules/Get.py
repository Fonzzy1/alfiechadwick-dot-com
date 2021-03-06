import spotipy
import pandas as pd


def sp_token():
    token = input('Enter Token: ')
    return token


def get_track_data(ls_track, token):
    track_df = pd.DataFrame(
        columns=['track', 'artist', 'song', 'album', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo'])
    for track in ls_track:
        sp = spotipy.Spotify(auth=token)
        track_name = sp.track(track)
        track_data = sp.audio_features(track)[0]
        artist = track_name['artists'][0]['name']
        song = track_name['name']
        album = track_name['album']
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
        track_row = [track, artist, song, album, danceability, energy, key, loudness, mode, speechiness,
                     acousticness,
                     instrumentalness, liveness, valence, tempo]
        track_df.loc[len(track_df)] = track_row
    track_df.set_index('track')
    return track_df



def sp_liked_tracks(token):
    track_list = []
    sp = spotipy.Spotify(auth=token)
    response = sp.current_user_saved_tracks()
    for item in response['items']:
        track = item['track']['id']
        track_list.append(track)
    while response['next']:
        response = sp.next(response)
        for item in response['items']:
            track = item['track']['id']
            track_list.append(track)

    return track_list


def sp_top_song_short(token):
    sp = spotipy.Spotify(auth=token)
    item = sp.current_user_top_tracks(1, 0, 'short_term')
    track = item['items'][0]['id']
    return track


def sp_top_song_medium(token):
    sp = spotipy.Spotify(auth=token)
    item = sp.current_user_top_tracks(1, 0, 'medium_term')
    track = item['items'][0]['id']
    return track


def sp_top_song_long(token):
    sp = spotipy.Spotify(auth=token)
    item = sp.current_user_top_tracks(1, 0, 'long_term')
    track = item['items'][0]['id']
    return track
