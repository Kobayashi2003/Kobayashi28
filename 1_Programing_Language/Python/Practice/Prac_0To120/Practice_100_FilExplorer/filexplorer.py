import os, sys
import keyboard
from threading import Thread, ThreadError
from time import sleep



def filexplorer_ui(prev_dir: dict, curr_dir: dict, next_dir: dict,
                prev_line: int, curr_line: int, next_line: int,
                terminal_width: int, terminal_height: int) -> None: # returns a file path
    # first list is 1/6 of the terminal width
    # second list is 3/6 of the terminal width
    # third list is 2/6 of the terminal width
    first_list_width = terminal_width // 6
    third_list_width = terminal_width // 3
    second_list_width = terminal_width - first_list_width - third_list_width

    line, first_line, second_line, third_line = 0, 0, 0, 0
    prev_dir_len = len(prev_dir)
    curr_dir_len = len(curr_dir)
    next_dir_len = len(next_dir)

    # print pattern
    color_function_generator = lambda num: lambda x: f"\033[38;5;{num}m{x}\033[0m"
    bg_color_function_generator = lambda num: lambda x: f"\033[48;5;{num}m{x}\033[0m"
    red_color = color_function_generator(196)
    red_bg_color = bg_color_function_generator(196)
    blue_color = color_function_generator(21)
    blue_bg_color = bg_color_function_generator(21)
    cry_color = color_function_generator(51)
    cry_bg_color = bg_color_function_generator(51)
    grey_color = color_function_generator(238)

    color_9 = color_function_generator(9)
    bg_color_9 = bg_color_function_generator(9)
    color_38 = color_function_generator(38)
    bg_color_38 = bg_color_function_generator(38)


    def count_length(string: str) -> int:
        length = 0
        for char in string:
            if ord(char) > 127:
                length += 2
            else:
                length += 1
        return length
    
    def filename_length_handler(string: str, width: int) -> str:
        file_name_length = count_length(string)
        if file_name_length < width:
            string += " " * (width - file_name_length)
            return string
        while file_name_length > width:
            string = string[:-1]
            file_name_length = count_length(string)
        string = string[:-3] + " ~ "
        return string
    
    def filename_print_handler(string:str, width: int,
                               is_dir: bool, is_selected: bool,
                               print_pattern_1=red_color, print_pattern_2=red_bg_color,
                               print_pattern_3=cry_color, print_pattern_4=cry_bg_color) -> str:
        string = filename_length_handler(string, width)
        front_blanks = string[:string.find(string.strip())]
        back_blanks = string[string.rfind(string.strip()) + len(string.strip()):]
        string = string.strip()
        if is_selected:
            if is_dir:
                return front_blanks + print_pattern_4(string) + back_blanks
            else:
                return front_blanks + print_pattern_2(string) + back_blanks
        else:
            if is_dir:
                return front_blanks + print_pattern_3(string) + back_blanks
            else:
                return front_blanks + print_pattern_1(string) + back_blanks
    
    os.system("cls")
    print('\033[?25l', end='')

    if prev_line > terminal_height:
        first_line = prev_line - terminal_height + 2

    if curr_line > terminal_height-(terminal_height//3) and curr_dir_len > terminal_height:
        if curr_dir_len - curr_line > terminal_height//3:
            second_line = curr_line - terminal_height + (terminal_height//3)
        else:
            second_line = curr_dir_len - terminal_height + 1

    if next_line > terminal_height:
        third_line = next_line - terminal_height + 2

    while first_line < prev_dir_len or \
        second_line < curr_dir_len or \
        third_line < next_dir_len:

        if line == 0:
            print('-' * (first_list_width-1) + ' ', end="")
            print(red_color('-' * (second_list_width-1) + ' '), end="")
            print('-' * third_list_width, end="")
            print()
            line += 1
            continue
        
        # first list
        if first_line < prev_dir_len:
            filename = list(prev_dir.keys())[first_line]
            file_is_dir = prev_dir[filename]
            print(filename_print_handler(filename, first_list_width, file_is_dir, first_line == prev_line, print_pattern_1=grey_color, print_pattern_3=grey_color), end="")
            first_line += 1
        else:
            print(" " * first_list_width, end="")

        # second list
        if second_line < curr_dir_len:
            blank_number = int(4-abs(second_line - curr_line)) * int(abs(second_line - curr_line) < 4)
            filename = list(curr_dir.keys())[second_line]
            file_is_dir = curr_dir[filename]
            filename = " " * blank_number + filename
            print(filename_print_handler(filename, second_list_width, file_is_dir, second_line == curr_line), end="")
            second_line += 1
        else:
            print(" " * second_list_width, end="")

        # third list
        if third_line < next_dir_len:
            filename = list(next_dir.keys())[third_line]
            file_is_dir = next_dir[filename]
            print(filename_print_handler(filename, third_list_width, file_is_dir, third_line == next_line, print_pattern_1=color_9, print_pattern_2=bg_color_9, print_pattern_3=color_38, print_pattern_4=bg_color_38), end="")
            third_line += 1
        else:
            print(" " * third_list_width, end="")

        line += 1
        if line >= terminal_height:
            break
        print()


def filexplorer_main() -> None:

    old_terminal_size = (0, 0)
    try:
        old_terminal_size = os.get_terminal_size()
    except:
        print("Terminal size error")
        return
    new_terminal_size = os.get_terminal_size()
    esc_flg = False
    def terminal_size_monitor():
        nonlocal old_terminal_size, new_terminal_size, esc_flg
        while True:
            if esc_flg:
                break
            new_terminal_size = os.get_terminal_size()
            sleep(0.05)
    th_terminal_size_monitor = Thread(target=terminal_size_monitor)
    th_terminal_size_monitor.start()

    # initialize the path and directory list
    curr_path = ""
    curr_dir_list = []
    curr_dir_dict = {}
    curr_line = 0
    try:
        curr_path = os.getcwd()
        curr_dir_list = os.listdir(curr_path)
    except:
        pass
    for file in curr_dir_list:
        curr_dir_dict[file] = os.path.isdir(os.path.join(curr_path, file))

    prev_path = ""
    prev_dir_list = []
    prev_dir_dict = {}
    prev_line = 0
    try:
        # judge if the current path is the root path
        if curr_path == os.path.dirname(curr_path):
            raise Exception
        prev_path = os.path.dirname(curr_path)     
        prev_dir_list = os.listdir(prev_path)
        prev_line = prev_dir_list.index(prev_path)
    except:
        pass
    for file in prev_dir_list:
        prev_dir_dict[file] = os.path.isdir(os.path.join(prev_path, file))

    next_path = ""
    next_dir_list = []
    next_dir_dict = {}
    next_line = 0
    try:
        next_path = curr_path + "\\" + curr_dir_list[curr_line]
        next_dir_list = os.listdir(next_path)
    except:
        pass
    for file in next_dir_list:
        next_dir_dict[file] = os.path.isdir(os.path.join(next_path, file))

    key_pressed_flg = False
    def key_pressed_monitor():
        nonlocal key_pressed_flg
        while True:
            if esc_flg:
                break
            keyboard.read_key()
            key_pressed_flg = True
    th_key_pressed_monitor = Thread(target=key_pressed_monitor)
    th_key_pressed_monitor.start()

    buffer = []

    update_flg = True

    while True:

        if old_terminal_size != new_terminal_size:
            old_terminal_size = new_terminal_size
            update_flg = True

        if update_flg:
            os.system("cls")
            terminal_width = new_terminal_size.columns
            terminal_height = new_terminal_size.lines
            filexplorer_ui(prev_dir_dict, curr_dir_dict, next_dir_dict, prev_line, curr_line, next_line, terminal_width, terminal_height)
            # print(prev_dir_dict)
            # print(curr_dir_dict)
            # print(next_dir_dict)
            update_flg = False

        sleep(0.05)

        if not key_pressed_flg and not update_flg:
            continue
        
        if keyboard.is_pressed('esc'):
            esc_flg = True
            th_terminal_size_monitor.join()
            print("th_terminal_size_monitor.join()")
            th_key_pressed_monitor.join()
            print("th_key_pressed_monitor.join()")
            os.system("cls")
            break
        elif keyboard.is_pressed('up'):
            curr_line -= 1
            if curr_line < 0:
                curr_line = 0
                continue
            elif curr_line >= len(curr_dir_list):
                curr_line = len(curr_dir_list) - 1
                continue
            next_path = ""
            next_dir_list = []
            next_dir_dict = {}
            next_line = 0
            try:
                next_path = curr_path + "\\" + curr_dir_list[curr_line]
                next_dir_list = os.listdir(next_path)
            except:
                pass
            for file in next_dir_list:
                next_dir_dict[file] = os.path.isdir(os.path.join(next_path, file))
            update_flg = True
        elif keyboard.is_pressed('down'):
            curr_line += 1
            if curr_line < 0:
                curr_line = 0
                continue
            elif curr_line >= len(curr_dir_list):
                curr_line = len(curr_dir_list) - 1
                continue
            next_path = ""
            next_dir_list = []
            next_dir_dict = {}
            next_line = 0
            try:
                next_path = curr_path + "\\" + curr_dir_list[curr_line]
                next_dir_list = os.listdir(next_path)
            except:
                pass
            for file in next_dir_list:
                next_dir_dict[file] = os.path.isdir(os.path.join(next_path, file))
            update_flg = True

        elif keyboard.is_pressed('left'):
            if prev_path != "" and len(prev_dir_list) != 0:
                next_path = curr_path
                next_dir_list = curr_dir_list
                next_dir_dict = curr_dir_dict
                next_line = curr_line

                curr_path = prev_path
                curr_dir_list = prev_dir_list
                curr_dir_dict = prev_dir_dict
                curr_line = prev_line

                prev_path = ""
                prev_dir_list = []
                prev_dir_dict = {}
                prev_line = 0
                try:
                    if curr_path == os.path.dirname(curr_path):
                        raise Exception
                    prev_path = os.path.dirname(curr_path)
                    prev_dir_list = os.listdir(prev_path)
                    prev_line = prev_dir_list.index(prev_path)
                except:
                    pass
                for file in prev_dir_list:
                    prev_dir_dict[file] = os.path.isdir(os.path.join(prev_path, file))
                update_flg = True
        elif keyboard.is_pressed('right'):
            if next_path != "" and len(next_dir_list) != 0:
                prev_path = curr_path
                prev_dir_list = curr_dir_list
                prev_dir_dict = curr_dir_dict
                prev_line = curr_line

                curr_path = next_path
                curr_dir_list = next_dir_list
                curr_dir_dict = next_dir_dict
                curr_line = next_line

                next_path = ""
                next_dir_list = []
                next_dir_dict = {}
                next_line = 0
                try:
                    next_path = curr_path + "\\" + curr_dir_list[curr_line]
                    next_dir_list = os.listdir(next_path)
                except:
                    pass
                for file in next_dir_list:
                    next_dir_dict[file] = os.path.isdir(os.path.join(next_path, file))
                update_flg = True

        elif keyboard.is_pressed('ctrl+enter'):
            main_event(buffer)
            buffer = []
            update_flg = True

        elif keyboard.is_pressed('enter'):
            buffer.append(curr_path + "\\" + curr_dir_list[curr_line])
            # update_flg = True

        elif keyboard.is_pressed('ctrl+up'):
            pass
        elif keyboard.is_pressed('ctrl+down'):
            pass
        elif keyboard.is_pressed('ctrl+left'):
            pass
        elif keyboard.is_pressed('ctrl+right'):
            pass


def virtual_file_tree_generator(file_tree: list, depth: int) -> None:
    pass # TODO
 

def main_event(buffer: list, func: callable=None) -> None:
    if func is None:
        os.system("cls")
        print("buffer:")
        for file in buffer:
            print(file)
        sleep(2)
    else:
        func(buffer)


def your_func(buffer: list) -> None:
    pass # TODO

            
if __name__ == "__main__":
    filexplorer_main()