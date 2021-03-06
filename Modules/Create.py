import sqlalchemy


def dataframe_to_sql(dataframe, table_name, database, password):
    db_connection_str = 'mysql+pymysql://fonzzy:' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    dataframe.to_sql(con=connection, name=table_name, )

