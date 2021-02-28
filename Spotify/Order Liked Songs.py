from datetime import date

from Spotify.Modules import authentication, Data, tracks, sorting, send_to_spotify

print('Retrieving Token')
token = authentication.get_token()

## Get set of liked tracks from spotify API
print('Retrieving Track List')
track_list = tracks.get_liked_tracks(token)

print('Retrieving Track Data')
track_df = Data.get_track_data_all(track_list, token)

print('Updating Z-Score')
Data.update_to_zscore(track_df)

print('Retrieving Start Track')
start_track = tracks.get_top_song_short(token)

print('Sorting Tracks')
sorting_cols = ['danceability_zscore', 'energy_zscore', 'loudness_zscore', 'mode_zscore', 'speechiness_zscore',
                'acousticness_zscore', 'instrumentalness_zscore', 'liveness_zscore', 'valence_zscore', 'tempo_zscore']
sorted_list = sorting.sort_tracks(track_df, start_track, sorting_cols)

print('Retrieving Token')
token = authentication.get_token()

print('Uploading to spotify')
playlist_name = 'Sorted ' + date.today()
send_to_spotify.create_playlist('', sorted_list, token)

print('Done')
exit(0)
