from datetime import date
import pyfiglet
import os
import pandas
import numpy as np
import pandas as pd
import spotipy
import sqlalchemy


def df_zscore(df, columns):
    for col in columns:
        col_zscore = col + '_zscore'
        df[col_zscore] = (df[col] - df[col].mean()) / df[col].std(ddof=0)


def df_distance(df, index_1, index_2, columns):
    data1 = df.loc[index_1, columns].values[0]
    data2 = df.iloc[index_2, columns].values[0]
    dist = np.linalg.norm(data1 - data2)
    return dist


def furthest_points(df, cols):
    start_sort_df = pd.DataFrame(columns=['Track_1', 'Track_2', 'Diff'])
    to_sort = df.index
    while len(to_sort) > 0:
        t1 = to_sort[0]
        to_sort = np.delete(to_sort, 0)
        for t2 in to_sort:
            diff = df_distance(df, t1, t2, cols)
            new_row = [t1, t2, diff]
            start_sort_df.loc[len(start_sort_df)] = new_row
    start_sort_df.sort_values(by=['Diff'], ascending=False, inplace=True, ignore_index=True)
    start_sort_df.reset_index(drop=True)
    furthest_set = start_sort_df.values.iloc[0]
    return furthest_set


def dataframe_to_sql(dataframe, table_name, database, password, SQL_Username):
    df = dataframe.reset_index()
    db_connection_str = 'mysql+pymysql://' + SQL_Username + ':' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    df.to_sql(con=connection, name=table_name, index=bool)


def list_to_sql(list, col_name, table_name, database, password, SQL_Username):
    df = pd.DataFrame(list, columns=[col_name])
    print(df)
    db_connection_str = 'mysql+pymysql://' + SQL_Username + ':' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    df.to_sql(con=connection, name=table_name, index=bool)


def dataframe_to_sql(dataframe, table_name, database, password, SQL_Username):
    df = dataframe.reset_index()
    db_connection_str = 'mysql+pymysql://' + SQL_Username + ':' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    for i in range(len(df)):
        try:
            df.iloc[i:i + 1].to_sql(name=table_name, if_exists='append', con=connection)
        except:
            pass


def sp_token():
    token = input('Enter Token: ')
    return token


def sp_track_data(ls_track, token):
    if not isinstance(ls_track, list):
        ls_track = [ls_track]
    else:
        ls_track = ls_track
    track_df = pd.DataFrame(
        columns=['track', 'song', 'artist', 'artist_id', 'album', 'album_id', 'genre', 'danceability', 'energy', 'key',
                 'loudness', 'mode', 'speechiness',
                 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo'])
    for track in ls_track:
        sp = spotipy.Spotify(auth=token)
        track_name = sp.track(track)
        track_data = sp.audio_features(track)[0]
        artist = track_name['artists'][0]['name']
        artist_id = track_name['artists'][0]['id']
        song = track_name['name']
        album = track_name['album']['name']
        album_id = track_name['album']['id']
        genre = sp.artist(artist_id)['genres']
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
        track_row = [track, song, artist, artist_id, album, album_id, genre, danceability, energy, key, loudness, mode,
                     speechiness,
                     acousticness,
                     instrumentalness, liveness, valence, tempo]
        track_df.loc[len(track_df)] = track_row
    track_df.set_index('track', inplace=True)
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


def sql_to_dataframe(table_name, database, password, SQL_Username):
    db_connection_str = 'mysql+pymysql://' + SQL_Username + ':' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    df = pandas.read_sql_table(table_name, con=connection)
    return df


def csv_to_dataframe(path):
    readcsv = pandas.read_csv(path)
    return readcsv


def sp_genres(df):
    genre_df = pd.DataFrame(columns=['track', 'genre', 'genre_count'])
    for track_id in df.index:
        genre_list = df.loc[track_id, 'genre']
        count = 1
        for genre in genre_list:
            new_row = [track_id, genre, count]
            genre
            count += 1
            genre_df.loc[len(genre_df)] = new_row
    return genre_df


def create_playlist(name, ls_track, token):
    sp = spotipy.Spotify(auth=token)
    user = ''.join(filter(lambda i: i.isdigit(), sp.current_user()['uri']))
    sp.user_playlist_create(user, name)
    playlist = sp.user_playlists(user)
    playlist_id = (playlist['items'][0]['id'])
    for song in ls_track:
        sp.playlist_add_items(playlist_id, [song])

def by_distace(df, start_index, col):
    sorted_list = []
    list = df.index.values.tolist()
    current_index = start_index
    while len(list) > 1:
        sorted_list.append(current_index)
        list.remove(current_index)
        holding_df = pd.DataFrame(columns=['index', 'Diff'])
        for index in list:
            data1 = df.loc[current_index, col].values[0]
            data2 = df.loc[index, col].values[0]
            dist = np.linalg.norm(data1 - data2)
            new_row = [index, dist]
            holding_df.loc[len(holding_df)] = new_row
        holding_df.sort_values(by=['Diff'], ascending=True, inplace=True, ignore_index=True)
        holding_df.reset_index(drop=True)
        current_index = holding_df.iloc[0]['index']
    sorted_list.append(list[0])
    return sorted_list


def run():
    os.system('clear')

    os.chdir('../../')
    os.chdir('./config')
    conf = csv_to_dataframe('config.csv')
    SQL_Username = conf.values[0][1]

    pyfiglet.print_figlet('Spotify: Order Songs', colors='MAGENTA')

    print('Retrieving Token')
    token = sp_token()

    ## Get set of liked tracks from spotify API
    print('Retrieving Track List')
    track_list = sp_liked_tracks(token)

    print('Retrieving Track Data')
    track_df = sp_track_data(track_list, token)

    genre_df = sp_genres(track_df)

    exit(0)

    print('Storing track data')
    dataframe_to_sql(track_df, 'ref_track_data', 'Spotify', '76692623Snow!SQL', SQL_Username)

    exit(0)
    print('Calculating Z-Score')
    columns = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence',
               'tempo']
    df_zscore(track_df, columns)

    print('Retrieving Start Track')
    start_track = sp_top_song_short(token)

    print('Sorting Tracks')
    sorting_colums = ['danceability_zscore', 'energy_zscore', 'speechiness_zscore', 'acousticness_zscore',
                      'instrumentalness_zscore', 'liveness_zscore', 'valence_zscore', 'tempo_zscore']
    sorted_list = by_distace(track_df, start_track, sorting_colums)

    print('Storing to SQL')
    table_name = 'Sorted ' + str(date.today())
    list_to_sql(sorted_list, 'track', table_name, 'Spotify', '76692623Snow!SQL', SQL_Username)

    print('Retrieving Token')
    token = sp_token()

    print('Uploading to spotify')
    playlist_name = 'Sorted ' + str(date.today())
    create_playlist(playlist_name, sorted_list, token)

    print('Done')
    exit(0)

run()

