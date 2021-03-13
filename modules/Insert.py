import sqlalchemy


def dataframe_to_sql(dataframe, table_name, database, password):
    df = dataframe.reset_index()
    db_connection_str = 'mysql+pymysql://fonzzy:' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    for i in range(len(df)):
        try:
            df.iloc[i:i + 1].to_sql(name=table_name, if_exists='append', con=connection)
        except:
            pass
