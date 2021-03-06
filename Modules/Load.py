import sqlalchemy
import pandas


def sql_to_dataframe(dataframe, table_name, database, password):
    db_connection_str = 'mysql+pymysql://fonzzy:' + password + '@localhost/' + database
    connection = sqlalchemy.create_engine(db_connection_str)
    pandas.read_sql_table(table_name, con=connection)
