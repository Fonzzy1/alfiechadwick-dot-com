import pandas as pd
import sqlalchemy


def dataframe_to_sql(dataframe, table_name, database, password):
    df = dataframe.reset_index()
    db_connection_str = 'mysql+pymysql://fonzzy:' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    df.to_sql(con=connection, name=table_name, index=bool)

def list_to_sql(list, col_name, table_name, database, password):
    df = pd.DataFrame(list, columns=[col_name])
    print(df)
    db_connection_str = 'mysql+pymysql://fonzzy:' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    df.to_sql(con=connection, name=table_name, index=bool)


