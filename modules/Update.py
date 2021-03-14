import sqlalchemy
import re


def sm_done_class(task_id, password):
    db_connection_str = 'mysql+pymysql://fonzzy:' + password + '@localhost/School'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update classes set revision = revision + 1, last_date = now() where task_id = ' + str(id)
    connection.execute(query)


def sm_done_assessment(task_id, password):
    db_connection_str = 'mysql+pymysql://fonzzy:' + password + '@localhost/School'
    connection = sqlalchemy.create_engine(db_connection_str)
    id = int("".join(filter(str.isdigit, task_id)))
    query = 'Update assessments set done = 1 where id = ' + str(id)
    connection.execute(query)
