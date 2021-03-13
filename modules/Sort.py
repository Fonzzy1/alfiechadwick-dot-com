import numpy as np
import pandas as pd


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
