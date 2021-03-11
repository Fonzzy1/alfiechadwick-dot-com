from Modules import Load, Update
import os
import time as t
os.system('clear')

password = input('Password: ')
offset = 0


def refresh(offset):
    os.system('clear')
    tasks = Load.sql_to_dataframe('task_list', 'School', password)
    current_task = tasks.iloc[offset]
    print(t.strftime("%Y-%m-%d %H:%M:%S",t.localtime()))
    print('Jobs to do: ' + str(len(tasks)))
    print('Current Task: ' + current_task['task_name'])
    print('Due: ' + str(current_task['task_date']))
    response = input('Y for done, S for Skip, R for Refresh Q for exit: ')

    if response == 'Q':
        exit()
    elif response == 'R':
        refresh()
    elif response == 'S':
        offset += 1
        refresh(offset)
    elif response == 'Y':
        offset = 0
        if current_task['id'][0]== 't':
            Update.sm_done_class(current_task['id'],password)
            refresh(offset)
        elif current_task['id'][0]== 'a':
            Update.sm_done_assessment(current_task['id'][0], password)
    else:
        refresh(offset)


refresh(offset)





