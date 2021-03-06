from datetime import date
import pandas as pd
from Modules import tracks, send_to_sql, data, sorting, authentication, send_to_spotify

print('Retrieving Token')
token = authentication.get_token()

## Get set of liked tracks from spotify API
print('Retrieving Track List')
track_list = tracks.get_liked_tracks(token)

print('Retrieving Track Data')
track_df = data.get_track_data(track_list, token)

print('Updating Z-Score')
data.update_to_zscore(track_df)

print('Retrieving Start Track')
start_track = '0eOfyH8KGgKJncEFu8peDj'
#tracks.get_top_song_short(token)

print('Sorting Tracks')
sorting_cols = ['danceability_zscore', 'energy_zscore', 'loudness_zscore', 'mode_zscore', 'speechiness_zscore',
                'acousticness_zscore', 'instrumentalness_zscore', 'liveness_zscore', 'valence_zscore', 'tempo_zscore']
sorted_list = sorting.sort_tracks(track_list, track_df, start_track, sorting_cols)


print('Retrieving Token')
token = authentication.get_token()

print('Uploading to SQL')
track_list_df = pd.DataFrame({'id':sorted_list})
table_name = 'Sorted ' + str(date.today())
send_to_sql.send_pandas_to_sql(track_list_df, table_name)


print('Uploading to spotify')
playlist_name = 'test'
send_to_spotify.create_playlist('', sorted_list, token)

print('Done')
exit(0)
