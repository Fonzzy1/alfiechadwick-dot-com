from runlist import timetable
import pyfiglet
import os
import time


def main_page():
    os.chdir("/home/fonzzy/Documents/Fonzzys-Projects")
    os.system('clear')

    ascii_art = pyfiglet.print_figlet('Fonzzy\'s Dashboard', colors='MAGENTA')

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
        return_ind = timetable.run()
        if return_ind == 1:
            main_page()

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
    for project in project_list:
        if project not in ['__init__.py', '__pycache__', 'timetable.py']:
            print(str(project_list.index(project))+ ': ' +project )
    response = input('Go to file or Q to quit: ')
    if response == 'Q':
        main_page()
    elif project_list[int(response)].endswith('.py'):
        os.system('python3 ./' + project_list[int(response)])
    else:
        try:
            os.chdir('./' + project_list[int(response)])
            project_page(project_list[int(response)])
        except:
            project_page('Oops, Try Again')


main_page()
