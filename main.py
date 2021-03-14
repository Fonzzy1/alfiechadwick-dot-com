from runlist import timetable
import pyfiglet
import os
import time


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
        return_ind = timetable.run()
        if return_ind == 1:
            main_page()

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
    for project in project_list:
        print(str(project_list.index(project))+ ': ' +project )
    response = input('Go to file, Q to quit, N for new file: ')
    if response == 'Q':
        main_page()
    elif response == 'N':
        file_name = input("File Name: ")
        os.system("touch " + file_name)
        main_page('New File Added')
    elif project_list[int(response)].endswith('.py'):
        os.system('python3 ./' + project_list[int(response)])
    elif project_list[int(response)].endswith('.R'):
        os.system('jetbrains-pycharm ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page()
    elif project_list[int(response)].endswith('.txt') or project_list[int(response)].endswith('.csv'):
        os.system('gedit ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page()
    elif project_list[int(response)].endswith('.SQL'):
        os.system('jetbrains-datagrip ./' + project_list[int(response)] + ' &')
        os.system('clear')
        main_page()

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
    call_list = ['/opt/REAPER/reaper', 'jetbrains-datagrip', 'github', 'jetbrains-pycharm', 'google-chrome', 'gedit', 'gnome-terminal']
    for program in program_list:
        print(str(program_list.index(program)) + ': ' + program)
    response = int(input('>>'))
    os.system(call_list[response] +' &')
    os.system('clear')
    main_page()


main_page()
