import os, sys
import keyboard
from threading import Thread, ThreadError
from time import sleep


now_line = 0
last_line = 0
next_line = 0

back_flag = False
enter_flag = False
esc_flag = False

now_path = os.getcwd()
last_path = ""
next_path = ""

def press_up(key: str) -> None:
    global now_line
    now_line -= 1
def press_down(key: str) -> None:
    global now_line
    now_line += 1
def press_left(key: str) -> None:
    global back_flag
    back_flag = True
def press_right(key: str) -> None:
    global enter_flag
    enter_flag = True
def press_enter(key: str) -> None:
    global enter_flag
    enter_flag = True
def press_esc(key: str) -> None:
    global esc_flag
    esc_flag = True
keyboard.on_press_key('up', press_up)
keyboard.on_press_key('down', press_down)
keyboard.on_press_key('left', press_left)
keyboard.on_press_key('right', press_right)
keyboard.on_press_key('enter', press_enter)
keyboard.on_press_key('esc', press_esc)

old_terminal_width, old_terminal_height = os.get_terminal_size().columns, os.get_terminal_size().lines
now_terminal_width, now_terminal_height = os.get_terminal_size().columns, os.get_terminal_size().lines

update_flag = False
def terminal_size() -> None:
    global old_terminal_height, old_terminal_width, now_terminal_height, now_terminal_width
    global esc_flag, update_flag
    while not esc_flag: 
        now_terminal_height, now_terminal_width = os.get_terminal_size().lines, os.get_terminal_size().columns
        if now_terminal_height != old_terminal_height or now_terminal_width != old_terminal_width:
            os.system('cls')
            print('Terminal size changed. Now the terminal size is: ', now_terminal_height, 'x', now_terminal_width)
            update_flag = True
            old_terminal_height, old_terminal_width = now_terminal_height, now_terminal_width
        sleep(0.5)
th_terminal_size = Thread(target=terminal_size)
try:
    th_terminal_size.start()
except ThreadError:
    pass


def count_string_length(string: str) -> int:
    length = 0
    for i in string:
        if ord(i) > 127:
            length += 2
        else:
            length += 1
    return length


def print_file_list(file_list: list, last_file_list: list, next_file_list: list) -> None:
    global now_line, last_line, next_line
    global now_terminal_height, now_terminal_width
    global now_path, last_path, next_path
    # if is a file, print the file name with red 
    # if is a folder, print the folder name with cryogenic blue
    # if the line is now_line, print the file name with the background color gray

    # last_file_list have 1/6 of the terminal width, and next_file_list have 2/6 of the terminal width, and file_list have 3/6 of the terminal width
    line = 0
    # TODO: slide window
    first_list_width = int(now_terminal_width / 6)
    second_list_width = int(now_terminal_width / 3)
    third_list_width = int(now_terminal_width / 2) + (now_terminal_width % 6) + (now_terminal_width % 3)
    first_line, second_line, third_line = 0, 0, 0
    while line < len(last_file_list) or line < len(file_list) or line < len(next_file_list):


        if first_line < len(last_file_list) and last_path != '':
            filename_length = count_string_length(last_file_list[first_line])
            if os.path.isfile(last_path + '\\' + last_file_list[first_line]):
                if filename_length > first_list_width - 2:
                    if first_line == last_line:
                        print('\033[0;30;41m' + last_file_list[first_line][:first_list_width - 4] + '\033[0m', end=' ~')
                    else:
                        print('\033[0;31m' + last_file_list[first_line][:first_list_width - 4] + '\033[0m', end=' ~')
                    print('  ', end='')
                else:
                    if first_line == last_line:
                        print('\033[0;30;41m' + last_file_list[first_line] + '\033[0m', end=' ' * (first_list_width - filename_length))
                    else:
                        print('\033[0;31m' + last_file_list[first_line] + '\033[0m', end=' ' * (first_list_width - filename_length))
            else:
                if filename_length > first_list_width - 2:
                    if first_line == last_line:
                        print('\033[0;30;46m' + last_file_list[first_line][:first_list_width - 4] + '\033[0m', end=' ~')
                    else:
                        print('\033[0;36m' + last_file_list[first_line][:first_list_width - 4] + '\033[0m', end=' ~')
                    print('  ', end='')
                else:
                    if first_line == last_line:
                        print('\033[0;30;46m' + last_file_list[first_line] + '\033[0m', end=' ' * (first_list_width - filename_length))
                    else:
                        print('\033[0;36m' + last_file_list[first_line] + '\033[0m', end=' ' * (first_list_width - filename_length))
            first_line += 1
        else:
            print(' ' * first_list_width, end='')

        if second_line < len(file_list):
            blank_number = int(4 - abs(second_line - now_line)) * int(abs(second_line - now_line) < 4)
            file_list[second_line] = " " * blank_number + file_list[second_line]
            filename_length = count_string_length(file_list[second_line])
            if os.path.isfile(now_path + '\\' + file_list[second_line].lstrip()):
                if filename_length > second_list_width - 2:
                    if second_line == now_line:
                        # print('\033[0;30;41m' + file_list[second_line][:second_list_width - 4] + '\033[0m', end=' ~')
                        print(file_list[second_line][:blank_number] + '\033[0;30;41m' + file_list[line][blank_number:second_list_width - 4] + '\033[0m', end=' ~')
                    else:
                        print('\033[0;31m' + file_list[second_line][:second_list_width - 4] + '\033[0m', end=' ~')
                    print('  ', end='')
                else:
                    if second_line == now_line:
                        # print('\033[0;30;41m' + file_list[second_line] + '\033[0m', end=' ' * (second_list_width - filename_length))
                        print(file_list[second_line][:blank_number] + '\033[0;30;41m' + file_list[line][blank_number:] + '\033[0m', end=' ' * (second_list_width - filename_length))
                    else:
                        print('\033[0;31m' + file_list[second_line] + '\033[0m', end=' ' * (second_list_width - filename_length))
            else:
                if filename_length > second_list_width - 2:
                    if second_line == now_line:
                        # print('\033[0;30;46m' + file_list[second_line][:second_list_width - 4] + '\033[0m', end=' ~')
                        print(file_list[second_line][:blank_number] + '\033[0;30;46m' + file_list[line][blank_number:second_list_width - 4] + '\033[0m', end=' ~')
                    else:
                        print('\033[0;36m' + file_list[second_line][:second_list_width - 4] + '\033[0m', end=' ~')
                    print('  ', end='')
                else:
                    if second_line == now_line:
                        # print('\033[0;30;46m' + file_list[second_line] + '\033[0m', end=' ' * (second_list_width - filename_length))
                        print(file_list[second_line][:blank_number] + '\033[0;30;46m' + file_list[line][blank_number:] + '\033[0m', end=' ' * (second_list_width - filename_length))
                    else:
                        print('\033[0;36m' + file_list[second_line] + '\033[0m', end=' ' * (second_list_width - filename_length))
            file_list[second_line] = file_list[second_line][blank_number:]
            second_line += 1
        else:
            print(' ' * second_list_width, end='')

        if third_line < len(next_file_list):
            filename_length = count_string_length(next_file_list[third_line])
            if os.path.isfile(next_path + '\\' + next_file_list[third_line]):
                if filename_length > third_list_width - 2:
                    if third_line == next_line:
                        print('\033[0;30;41m' + next_file_list[third_line][:third_list_width - 4] + '\033[0m', end=' ~')
                    else:
                        print('\033[0;31m' + next_file_list[third_line][:third_list_width - 4] + '\033[0m', end=' ~')
                    print('  ', end='')
                else:
                    if third_line == next_line:
                        print('\033[0;30;41m' + next_file_list[third_line] + '\033[0m', end=' ' * (third_list_width - filename_length))
                    else:
                        print('\033[0;31m' + next_file_list[third_line] + '\033[0m', end=' ' * (third_list_width - filename_length))
            else:
                if filename_length > third_list_width - 2:
                    if third_line == next_line:
                        print('\033[0;30;46m' + next_file_list[third_line][:third_list_width - 4] + '\033[0m', end=' ~')
                    else:
                        print('\033[0;36m' + next_file_list[third_line][:third_list_width - 4] + '\033[0m', end=' ~')
                    print('  ', end='')
                else:
                    if third_line == next_line:
                        print('\033[0;30;46m' + next_file_list[line] + '\033[0m', end=' ' * (third_list_width - filename_length))
                    else:
                        print('\033[0;36m' + next_file_list[line] + '\033[0m', end=' ' * (third_list_width - filename_length))
            third_line += 1
        else:
            print(' ' * third_list_width, end='')
        

        if line == now_terminal_height - 1:
            break
        print()
        line += 1

    print('\033[?25l', end='')


def file_explorer() -> None:
    global enter_flag, esc_flag, back_flag, update_flag
    global now_line, last_line, next_line
    global th_terminal_size
    global now_path, last_path, next_path 

    now_path = os.getcwd().replace('\\', '//')
    file_list = os.listdir()

    last_path = '//'.join(now_path.split('//')[:-1])
    last_file_list = os.listdir('..')
    last_line = last_file_list.index(now_path.split('//')[-1]) 

    next_file_list = []
    if os.path.isdir(file_list[now_line]):
        next_file_list = os.listdir(file_list[now_line])
        next_path = now_path + '//' + file_list[now_line]

    # BUG: when the folder is empty, the program will crash
    while True:
        if now_line < 0 or now_line >= len(file_list):
            now_line = old_line
        old_line = now_line

        if os.path.isdir(file_list[now_line]):
            try:
                next_file_list = os.listdir(file_list[now_line])
                next_path = now_path + '//' + file_list[now_line]
            except PermissionError:
                next_file_list = []
                next_path = ''
            except FileNotFoundError:
                next_file_list = []
                next_path = ''
        else:
            next_file_list = []
            next_line = 0
            next_path = ''

        os.system('cls')
        print_file_list(file_list, last_file_list, next_file_list)

        while not enter_flag and not esc_flag and not back_flag and old_line == now_line and not update_flag:
            pass

        if old_line != now_line:
            next_line = 0

        if enter_flag:
            if os.path.isfile(file_list[now_line]):
                pass
            else:
                # update path
                last_path = now_path
                now_path = next_path
                # update file_list
                last_file_list = file_list
                try :
                    os.chdir(file_list[now_line])
                    file_list = next_file_list
                except PermissionError:
                    pass
                # update file line
                last_line = now_line
                now_line = next_line
                next_line = 0
            enter_flag = False

        if back_flag:
            # update path
            if last_path == '':
                back_flag = False
                continue
            now_path = last_path
            last_path = '//'.join(now_path.split('//')[:-1])
            if last_path == '':
                # last_line = 0
                last_file_list = []
            # update file_list
            os.chdir('..')
            file_list = os.listdir()
            last_file_list = os.listdir('..')
            # update file line
            next_line = now_line
            now_line = last_line
            try:
                last_line = last_file_list.index(os.getcwd().split('\\')[-1])
            except:
                last_line = 0

            back_flag = False

        if update_flag:
            update_flag = False
        if esc_flag:
            break
    os.system('cls')
    th_terminal_size.join()
    print('Bye~')        

if __name__ == '__main__':
    file_explorer()