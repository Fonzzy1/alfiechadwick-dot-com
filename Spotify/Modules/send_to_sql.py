from mysql.connector import connect
from sqlalchemy import create_engine


def send(query):
    connection = connect(user='fonzzy', password='76692623Snow!SQL', database='Spotify')
    cursor = connection.cursor()
    cursor.execute(query)


def recive(query):
    connection = connect(user='fonzzy', password='76692623Snow!SQL', database='Spotify')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def commit():
    connection = connect(user='fonzzy', password='76692623Snow!SQL', database='Spotify')
    connection.commit()


def send_pandas_to_sql(dataframe, tablename):
    db_connection_str = 'mysql+pymysql://fonzzy:76692623Snow!SQL@localhost/Spotify'
    connection = create_engine(db_connection_str)
    dataframe.to_sql(con=connection, name=tablename)
    commit()
