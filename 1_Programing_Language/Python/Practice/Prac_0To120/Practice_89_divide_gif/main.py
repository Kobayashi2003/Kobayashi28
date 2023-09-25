from devide_gif import devide_gif
from ascii_srt import ascii_srt, draw_in_terminal
import sys, os
import time

def show_gif(jpg_list):
    results = []
    for jpg in jpg_list:
        results.append(ascii_srt(jpg))

    i = 0
    while True:
        if results[i][0] == "terminal":
            os.system("cls")
            draw_in_terminal(*results[i][1:])
        i += 1

        frame = lambda x: 1 / x
        time.sleep(frame(9))

        if i == len(jpg_list):
            if input() == " ":
                i = 0
            else:
                break

def remove_jpg(jpg_list):
    os.system("cls")
    for jpg in jpg_list:
        os.remove(jpg)

if __name__ == "__main__":
    path = sys.argv[1]
    jpg_list = devide_gif(path)
    show_gif(jpg_list)
    remove_jpg(jpg_list)