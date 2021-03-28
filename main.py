import time
import pyfiglet
import readchar
from modules import Load, Update
import os
import time as t


def main_page(password):
    response = ''
    os.chdir("/home/fonzzy/Documents")
    os.system('clear')
    current_task = Load.sql_to_dataframe('task_list', 'School', password).iloc[0]


    pyfiglet.print_figlet('Fonzzy\'s Dashboard', colors='MAGENTA')

    print(
        'A collection of projects, made mostly for myself and will most likely not work on other machines, created so I '
        'can easily run my work\n\n' +
        time.strftime("%Y-%m-%d %H:%M", time.localtime()) +
        '\n\n'
        'Current Job: ' + current_task[1] +
        '\n\n'
        'Show info - r'
        '\n\n'
        'Time Table - t'
        '\n\n'
        'Finished Current Job - y'       
        '\n\n'
        'Other Projects - p'
        '\n\n'
        'Programs - o'
        '\n\n'
        'Quit - q'
        '\n'
    )
    print('>> ')
    response = readchar.readkey()

    if response == 'r':

        f = open("README.md", "r")
        os.system('clear')
        print(f.read())
        print('Enter any key to return: ')
        response = readchar.readkey()
        if response:
            main_page(password)

    elif response == 't':
        refresh(0,password)

    elif response == 'y':
        if current_task['id'][0] == 't':
            Update.sm_done_class(current_task['id'], password)
            main_page(password)
        elif current_task['id'][0] == 'a':
            Update.sm_done_assessment(current_task['id'], password)
            main_page(password)


    elif response == 'o':
        programs_page(password)


    elif response == 'p':
        initial_head = 'Fonzzy\'s Projects'
        project_page(initial_head,password)

    elif response == 'q':
        os.system('clear')
        quit(1)

    else:
        main_page(password)


def project_page(response, password):
    project_list = os.listdir()
    os.system('clear')
    ascii_art = pyfiglet.print_figlet(response, colors='MAGENTA')
    unwanted = ['__init__.py', '__pycache__', 'timetable.py']
    for item in unwanted:
        try:
            project_list.remove(item)
        except:
            break
    for item in project_list:
        if item.startswith('.'):
            project_list.remove(item)
    project_list = sorted(project_list)
    for project in project_list:
        print(str(project_list.index(project)) + ': ' + project)
    print('Go to file, q to quit, n for new file: ')
    response = readchar.readkey()
    if response == 'q':
        main_page(password)
    elif response == 'n':
        file_name = input("File Name: ")
        os.system("touch " + file_name)
        project_page('New File Added',password)
    elif project_list[int(response)].endswith('.py'):
        os.system('python3 ./' + project_list[int(response)])
    elif project_list[int(response)].endswith('.R'):
        os.system('jetbrains-pycharm ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page(password)
    elif project_list[int(response)].endswith('.pdf'):
        os.system('evince ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page(password)
    elif project_list[int(response)].endswith('.png') + project_list[int(response)].endswith('.jpg'):
        os.system('eog ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page(password)
    elif project_list[int(response)].endswith('.txt') or project_list[int(response)].endswith('.csv') or project_list[
        int(response)].endswith('.md'):
        os.system('gedit ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page(password)
    elif project_list[int(response)].endswith('.SQL'):
        os.system('jetbrains-datagrip ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page(password)
        # TODO: do some form of associative sctructure - file type to program

    else:
        try:
            os.chdir('./' + project_list[int(response)])
            project_page(project_list[int(response)],password)
        except:
            project_page('Oops, Try Again',password)


def programs_page(password):
    os.system('clear')
    pyfiglet.print_figlet('Programs', colors='MAGENTA')
    program_list = ['Reaper', 'Datagrip', 'Github', 'Pycharm', 'Chrome', 'Gedit', 'Terminal', 'Reddit']
    call_list = ['/opt/REAPER/reaper', 'jetbrains-datagrip', 'github', 'jetbrains-pycharm', 'google-chrome', 'gedit',
                 'gnome-terminal', 'gnome-terminal -e "bash -c \"rtv; exec bash\""'
]
    for program in program_list:
        print(str(program_list.index(program)) + ': ' + program)
    response = readchar.readkey()
    try:
        response = int(response)
    except:
        main_page(password)
    os.system(call_list[response] + ' &')
    os.system('clear')
    main_page(password)


def refresh(offset, password):
    os.system('clear')
    pyfiglet.print_figlet('Timetable', colors='MAGENTA')
    tasks = Load.sql_to_dataframe('task_list', 'School', password)
    if len(tasks) > 0:
        current_task = tasks.iloc[offset]
        print(t.strftime("%Y-%m-%d", t.localtime()))
        print('Jobs to do: ' + str(len(tasks)))
        print('Current Task: ' + current_task['task_name'])
        print('Due: ' + str(current_task['task_date'])[0:10])
        print('y for done\ns for Skip\nr for Refresh\nq for exit\nl for list all: ')
        response = readchar.readkey()

        if response == 'q':
            response = 1
            if response == 1:
                main_page(password)
        elif response == 'r':
            offset = 0
            refresh(offset, password)
        elif response == 's':
            if offset < len(tasks)-1:
                offset += 1
            refresh(offset, password)
        elif response == 'l':
            os.system('clear')
            pyfiglet.print_figlet('Timetable', colors='MAGENTA')
            print('Jobs to do: ' + str(len(tasks)))

            for row in sorted(tasks['task_name']):
                print(tasks.loc[tasks['task_name'] == row]['task_name'].values[0] + ' : '+ str(tasks.loc[tasks['task_name'] == row]['task_date'].values[0])[0:10])
            print('Press Y to set all to done or press any key to return to main: ')
            exe = readchar.readkey()
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
        elif response == 'y':
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
        print('return to main')
        response = readchar.readkey()
        if response:
            main_page(password)





def start():
    os.system('clear')
    pyfiglet.print_figlet('Fonzzy\'s Dashboard', colors='MAGENTA')
    while True:
        try:
            password = input('Password: ')
            Load.sql_to_dataframe('task_list', 'School', password)
            break
        except:
            print("Oops!  That not the password.  Try again...")

    main_page(password)

start()