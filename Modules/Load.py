import pandas
import sqlalchemy


def sql_to_dataframe(table_name, database, password):
    db_connection_str = 'mysql+pymysql://fonzzy:' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    df = pandas.read_sql_table(table_name, con=connection)
    return df

def csv_to_dataframe(path):
    readcsv = pandas.read_csv(path, index_col=[0])
    return readcsv
