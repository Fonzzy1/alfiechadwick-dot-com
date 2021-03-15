import time
import pyfiglet

from modules import Load, Update
import os
import time as t


def main_page():
    os.chdir("/home/fonzzy/Documents/Fonzzys-Projects")
    os.system('clear')

    pyfiglet.print_figlet('Fonzzy\'s Dashboard', colors='MAGENTA')

    print(
        'A collection of projects, made mostly for myself and will most likely not work on other machines, created so I '
        'can easily run my work\n\n' +
        time.strftime("%Y-%m-%d %H:%M", time.localtime()) +
        '\n\n'
        'Show info - r'
        '\n\n'
        'Time Table - t'
        '\n\n'
        'Other Projects - p'
        '\n\n'
        'Programs - o'
        '\n\n'
        'Quit - q'
        '\n'
    )
    response = input('>> ')

    if response == 'r':

        f = open("README.md", "r")
        os.system('clear')
        print(f.read())
        response = input('Enter any key to return: ')
        if response:
            main_page()

    elif response == 't':
        timetable()

    elif response == 'o':
        programs_page()

    elif response == 'p':
        os.chdir('./runlist')
        initial_head = 'Fonzzy\'s Projects'
        project_page(initial_head)

    elif response == 'q':
        os.system('clear')
        quit(1)

    else:
        main_page()


def project_page(response):
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
    response = input('Go to file, q to quit, n for new file: ')
    if response == 'q':
        main_page()
    elif response == 'n':
        file_name = input("File Name: ")
        os.system("touch " + file_name)
        project_page('New File Added')
    elif project_list[int(response)].endswith('.py'):
        os.system('python3 ./' + project_list[int(response)])
    elif project_list[int(response)].endswith('.R'):
        os.system('jetbrains-pycharm ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page()
    elif project_list[int(response)].endswith('.pdf'):
        os.system('evince ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page()
    elif project_list[int(response)].endswith('.png') + project_list[int(response)].endswith('.jpg'):
        os.system('eog ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page()
    elif project_list[int(response)].endswith('.txt') or project_list[int(response)].endswith('.csv') or project_list[
        int(response)].endswith('.md'):
        os.system('gedit ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page()
    elif project_list[int(response)].endswith('.SQL'):
        os.system('jetbrains-datagrip ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page()
        # TODO: do some form of associative sctructure - file type to program

    else:
        try:
            os.chdir('./' + project_list[int(response)])
            project_page(project_list[int(response)])
        except:
            project_page('Oops, Try Again')


def programs_page():
    os.system('clear')
    pyfiglet.print_figlet('Programs', colors='MAGENTA')
    program_list = ['Reaper', 'Datagrip', 'Github', 'Pycharm', 'Chrome', 'Gedit', 'Terminal']
    call_list = ['/opt/REAPER/reaper', 'jetbrains-datagrip', 'github', 'jetbrains-pycharm', 'google-chrome', 'gedit',
                 'gnome-terminal']
    for program in program_list:
        print(str(program_list.index(program)) + ': ' + program)
    response = int(input('>>'))
    os.system(call_list[response] + ' &')
    os.system('clear')
    main_page()


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
            if response == 1:
                main_page()
        elif response == 'r':
            offset = 0
            refresh(offset, password)
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
        response = input('return to main')
        if response:
            main_page()


def timetable():
    os.system('clear')
    pyfiglet.print_figlet('Timetable', colors='MAGENTA')
    while True:
        try:
            password = input('Password: ')
            Load.sql_to_dataframe('task_list', 'School', password)
            break
        except:
            print("Oops!  That not the password.  Try again...")

    refresh(0,password)



main_page()
