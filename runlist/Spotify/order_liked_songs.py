from datetime import date

import pyfiglet

from modules import Get, Insert, Calculate, Sort, Create, Send, Reshape, Save
import os

import pandas


def run():
    os.system('clear')

    pyfiglet.print_figlet('Spotify: Order Songs', colors='MAGENTA')

    print('Retrieving Token')
    token = Get.sp_token()

    ## Get set of liked tracks from spotify API
    print('Retrieving Track List')
    track_list = Get.sp_liked_tracks(token)

    print('Retrieving Track Data')
    track_df = Get.sp_track_data(track_list, token)

    genre_df = Reshape.sp_genres(track_df)

    exit(0)

    print('Storing track data')
    Insert.dataframe_to_sql(track_df, 'ref_track_data', 'Spotify', '76692623Snow!SQL')

    exit(0)
    print('Calculating Z-Score')
    columns = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence',
               'tempo']
    Calculate.df_zscore(track_df, columns)

    print('Retrieving Start Track')
    start_track = Get.sp_top_song_short(token)

    print('Sorting Tracks')
    sorting_colums = ['danceability_zscore', 'energy_zscore', 'speechiness_zscore', 'acousticness_zscore',
                      'instrumentalness_zscore', 'liveness_zscore', 'valence_zscore', 'tempo_zscore']
    sorted_list = Sort.by_distace(track_df, start_track, sorting_colums)

    print('Storing to SQL')
    table_name = 'Sorted ' + str(date.today())
    Create.list_to_sql(sorted_list, 'track', table_name, 'Spotify', '76692623Snow!SQL')

    print('Retrieving Token')
    token = Get.sp_token()

    print('Uploading to spotify')
    playlist_name = 'Sorted ' + str(date.today())
    Send.create_playlist(playlist_name, sorted_list, token)

    print('Done')
    exit(0)

run()

