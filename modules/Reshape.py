import pandas as pd


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
