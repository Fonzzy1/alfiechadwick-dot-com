import numpy as np
import pandas as pd


def find_distance(track_df, track1, track2, cols):
    track_data1 = track_df.loc[
        track_df['track'] == track1, cols].values[0]
    track_data2 = track_df.loc[
        track_df['track'] == track2, cols].values[0]
    dist = np.linalg.norm(track_data1 - track_data2)
    return dist


def find_furthest_tracks(track_df, cols):
    start_sort_df = pd.DataFrame(columns=['Track_1', 'Track_2', 'Diff'])
    tracks_to_sort = np.array(track_df['track'])
    while len(tracks_to_sort) > 0:
        t1 = tracks_to_sort[0]
        tracks_to_sort = np.delete(tracks_to_sort, 0)
        for t2 in tracks_to_sort:
            diff = find_distance(track_df, t1, t2, cols)
            new_row = [t1, t2, diff]
            start_sort_df.loc[len(start_sort_df)] = new_row
    start_sort_df.sort_values(by=['Diff'], ascending=False, inplace=True, ignore_index=True)
    start_sort_df.reset_index(drop=True)
    furthest_track = start_sort_df.iloc[0]
    return furthest_track


def sort_tracks(track_df, start_track, cols):
    sorted_list = []
    track_list = np.array(track_df['track']).tolist()
    current_track = start_track
    while len(track_list) > 1:
        sorted_list.append(current_track)
        track_list.remove(current_track)
        holding_df = pd.DataFrame(columns=['Track', 'Diff'])
        for track in track_list:
            new_row = [track, find_distance(track_df, current_track, track, cols)]
            holding_df.loc[len(holding_df)] = new_row
        holding_df.sort_values(by=['Diff'], ascending=True, inplace=True, ignore_index=True)
        holding_df.reset_index(drop=True)
        current_track = holding_df.iloc[0]['Track']
    return sorted_list
