from runlist import timetable, order_liked_songs
import pyfiglet
import os
import time


def main_page():
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
        project_list = os.listdir('./runlist')
        for project in project_list:
            if project.endswith('.py') and project!= '__init__.py':
                print(project)

    elif response == 'q':
        os.system('clear')
        quit(1)

    else:
        main_page()


main_page()
