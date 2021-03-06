import Calculate as C





def by_distace(df, start_index, col):
    sorted_list = []
    list = df.index.values
    current_index = start_index
    while len(list) > 1:
        sorted_list.append(current_index)
        list.remove(current_index)
        holding_df = pd.DataFrame(columns=['index', 'Diff'])
        for index in list:
            new_row = [index, C.df_distance(df,current_index,index,col)]
            holding_df.loc[len(holding_df)] = new_row
        holding_df.sort_values(by=['Diff'], ascending=True, inplace=True, ignore_index=True)
        holding_df.reset_index(drop=True)
        current_index = holding_df.iloc[0]['Track']
    sorted_list.append(list[0])
    return sorted_list
