import pyfiglet

from modules import Load, Update
import os
import time as t


def refresh(offset, password):
    os.system('clear')
    pyfiglet.print_figlet('Timetable', colors='MAGENTA')
    tasks = Load.sql_to_dataframe('task_list', 'School', password)
    if len(tasks) > 0:
        current_task = tasks.iloc[offset]
        print(t.strftime("%Y-%m-%d %H:%M:%S", t.localtime()))
        print('Jobs to do: ' + str(len(tasks)))
        print('Current Task: ' + current_task['task_name'])
        print('Due: ' + str(current_task['task_date']))
        response = input('y for done\ns for Skip\nr for Refresh\nq for exit\nl for list all: ')

        if response == 'q':
            response = 1
            if response:
                return_ind = 1
        elif response == 'r':
            offset = 0
            refresh(offset ,password)
        elif response == 's':
            offset += 1
            refresh(offset, password)
        elif response == 'l':
            os.system('clear')
            pyfiglet.print_figlet('Timetable', colors='MAGENTA')
            print('Jobs to do: ' + str(len(tasks)))
            for row in tasks['id']:
                print(tasks.loc[tasks['id'] == row]['task_name'].values[0])
            exe = input('Press Y to set all to done or press any key to return to main: ')
            if exe == 'Y':
                for row in tasks.index:
                    current_task = tasks.loc[row]
                    if current_task['id'][0] == 't':
                        Update.sm_done_class(current_task['id'], password)
                    elif current_task['id'][0] == 'a':
                        Update.sm_done_assessment(current_task['id'], password)
                refresh(offset, password)
            else:
                refresh(offset, password)
        elif response == 'Y':
            offset = 0
            if current_task['id'][0] == 't':
                Update.sm_done_class(current_task['id'], password)
                refresh(offset, password)
            elif current_task['id'][0] == 'a':
                Update.sm_done_assessment(current_task['id'], password)
                refresh(offset, password)
        else:
            refresh(offset, password)
    else:
        print('No Jobs')
        response = input('return to main')
        if response:
            return_ind = 1
    return return_ind


def run():
    os.system('clear')
    pyfiglet.print_figlet('Timetable', colors='MAGENTA')
    while True:
        try:
            password = input('Password: ')
            Load.sql_to_dataframe('task_list', 'School', password)
            break
        except:
            print("Oops!  That not the password.  Try again...")

    offset = 0

    return_ind = refresh(offset, password)
    return return_ind
