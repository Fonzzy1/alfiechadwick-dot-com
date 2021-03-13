import numpy as np
import pandas as pd


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
