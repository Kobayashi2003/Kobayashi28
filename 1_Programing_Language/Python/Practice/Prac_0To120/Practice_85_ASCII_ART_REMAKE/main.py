# from ascii_srt import ascii_srt
from ascii_srt import draw_in_terminal, draw_in_image

import os, sys
import glob

import keyboard
import time

# from threading import Thread
from ascii_srt_thread import ascii_srt_thread

if __name__ == "__main__":

    help_msg = """

     _         _                           _     _
    | | _____ | |__   __ _ _   _  __ _ ___| |__ (_)
    | |/ / _ \| '_ \ / _` | | | |/ _` / __| '_ \| |
    |   < (_) | |_) | (_| | |_| | (_| \__ \ | | | |
    |_|\_\___/|_.__/ \__,_|\__, |\__,_|___/_| |_|_|
                           |___/

        _    ____   ____ ___ ___      _    ____ _____
       / \  / ___| / ___|_ _|_ _|    / \  |  _ \_   _|
      / _ \ \___ \| |    | | | |    / _ \ | |_) || |
     / ___ \ ___) | |___ | | | |   / ___ \|  _ < | |
    /_/   \_\____/ \____|___|___| /_/   \_\_| \_\|_|


    Usage:

        python main.py [options] [image path]

    Options:

        -r --rate [float]: sample rate
                
                set the sample rate, if the rate is not set, the size of the output will depend on the size of the terminal
                once the rate is set, the value of the rate MUST be set
                the rate should be between 0 and 1

        -d --dir [dir_path]: use all images in the directory

                set the directory to use
                once the directory is set, the value of the directory MUST be set
                this script will find all images(.jpg, .png) in the directory and convert them to ascii art

        -s --save [save_dir_path]: save the ascii art to a file

                save the ascii art to the directory specified by [save_dir_path]
                if [save_dir_path] is not set, the ascii art will be saved to the same directory as the original image

        -nc --no_color : use color in the output

                set whether to use color in the output
                                                                                              
        -bc --background_color [RGB=(r, g, b) / color_name]: background color

                set the background color of the output
                once the background color is set, the value of the background color MUST be set
                format: RGB=(r, g, b) or color_name

        -f --font [font_path]: use a custom font

                set the font to use
                once the font is set, the value of the font MUST be set

        --simple: use simple ascii characters

                set whether to use simple ascii characters
                in simple mode, the characters used are " .-v*M@#"
                in normal mode, the characters used are " `.^\\:~<!ct+{i7?u30pw4A8DX\%#HWM"

        -m --mode [mode]: printing mode

                set the printing mode
                once the printing mode is set, the value of the printing mode MUST be set

                "image" : print the ASCII art as an image.
                "terminal" : print the ASCII art in the terminal.
                "auto" : the mode will depend on the size of the ASCII art.
                "default" : "auto"

        -h --help: show help message
"""

    # TODO: pipe input

    if len(sys.argv) == 1:
        print(help_msg)
        exit()

    # param
    param = {
        "image_path" : [],
        "save_path" : "false",
        "font_path" : "default",
        "rate" : 0,
        "simple_mode" : False,
        "printing_mode" : "default",
        "no_color" : False,
        "background_color" : "default"
    }


    # get the param
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ["-h", "--help"]:
            print(help_msg)
            exit()

        elif sys.argv[i] in ["-r", "--rate"]:
            try:
                param["rate"] = float(sys.argv[i + 1])
                if param["rate"] < 0 or param["rate"] > 1:
                    print("\033[31mError: Invaild rate value, the value of rate should between (0,1]\033[0m")
                    exit()
                i += 1
            except:
                print("\033[31mError: Invaild rate value\033[0m")
                exit()

        elif sys.argv[i] in ["-d", "--dir"]:
            try:
                dir_path = sys.argv[i + 1]
                for file in glob.glob(dir_path + "/*.jpg"):
                    param["image_path"].append(file)
                for file in glob.glob(dir_path + "/*.png"):
                    param["image_path"].append(file)
                i += 1
            except:
                print("\033[31mError: Invaild directory path\033[0m")
                exit()
            
        elif sys.argv[i] in ["-s", "--save"]:
            try:
                if sys.argv[i + 1][0] != "-":
                    param["save_path"] = sys.argv[i + 1]
                    i += 1
            except:
                pass

        elif sys.argv[i] in ["-nc", "--no_color"]:
            param["no_color"] = True

        elif sys.argv[i] in ["-bc", "--background_color"]:
            try:
                if sys.argv[i + 1][0] != "-":
                    param["background_color"] = sys.argv[i + 1]
                    i += 1
                else:
                    print("\033[31mError: Invaild background color value\033[0m")
                    exit()
            except:
                print("\033[31mError: Invaild background color value\033[0m")
                exit()

        elif sys.argv[i] in ["-f", "--font"]:
            try:
                if sys.argv[i + 1][0] != "-":
                    param["font_path"] = sys.argv[i + 1]
                    # check if the font path is valid
                    if not os.path.exists(param["font_path"]):
                        print("\033[31mError: Invaild font path\033[0m")
                        exit()
                    i += 1
                else:
                    print("\033[31mError: Invaild font path\033[0m")
                    exit()
            except:
                print("\033[31mError: Invaild font path\033[0m")
                exit()


        elif sys.argv[i] in ["--simple"]:
            param["simple_mode"] = True


        elif sys.argv[i] in ["-m", "--mode"]:
            try:
                if sys.argv[i+1] in ["image", "terminal", "auto", "default"]:
                    param["printing_mode"] = sys.argv[i+1]
                    i += 1
                else:
                    param["printing_mode"] = "default"
            except:
                param["printing_mode"] = "default"


        elif sys.argv[i][0] == "-":
            print("\033[31mError: Invaild option\033[0m")
            exit()
        
        else:
            param["image_path"].append(sys.argv[i])

        i += 1


    # anlysis the image path, expand the wildcard
    images_path = []
    for paths in param["image_path"]:
        for path in glob.glob(paths):
            images_path.append(path)

    count = 0
    threads = []
    for path in images_path:
        param["image_path"] = path
        thread = ascii_srt_thread(param, count)
        count += 1
        thread.start()
        threads.append(thread)



    # press j to show the next image
    # press k to show the previous image
    # press g to goto the num page
    # press r to reload the current page 
    # press q to quit


    # keyboard monitor
    key_press_flg = True
    page = 0
    quit = False
    def key_press(key):
        global page, quit, key_press_flg, count

        global param, images_path, threads

        if key.name == "j" or key.name == "down":
            if page == count - 1:
                print("\033[31mThis is the last page\033[0m")
            else:
                page += 1
                key_press_flg = True
        elif key.name == "k" or key.name == "up":
            if page == 0:
                print("\033[31mThis is the first page\033[0m")
            else:
                page -= 1
                key_press_flg = True

        elif key.name == "g" or key.name == "tab":
            num = page
            try:
                num = int(input("page: "))
                if num < 0 or num >= count:
                    print("\033[31mError: Invaild page number\033[0m")
                    num = page
            except:
                print("\033[31mError: Invaild page number\033[0m")
                num = page
            page = num
            key_press_flg = True

        elif key.name == "r" or key.name == "space":
            if threads[page].is_alive():
                print("\033[31mRurning...\033[0m")
            else:
                threads[page].join()
                param["image_path"] = images_path[page]
                threads[page] = ascii_srt_thread(param, page)
                threads[page].start()
            key_press_flg = True

        elif key.name == "q" or key.name == "esc":
            quit = True
            key_press_flg = True
        elif key.name == "space":
            key_press_flg = True
        else:
            pass
    keyboard.on_press(key_press)
        
    while not quit:

        if key_press_flg:
            key_press_flg = False

            os.system("cls")
            print("Page:[{}/{}]".format(page + 1, count))

            result = None
            t = time.time()
            while result is None:
                result = threads[page].get_result()
                print(['\\', '|', '/', '-'][int(time.time() - t) % 4], end='\b')
                if key_press_flg:
                    break
            
            if quit:
                break

            os.system("cls")
            print("Page:[{}/{}]".format(page + 1, count))
            if result is not None:
                if result[0] == "image":
                    im_out = result[1]
                    draw_in_image(im_out)
                elif result[0] == "terminal":
                    ascii, im_color = result[1:3]
                    draw_in_terminal(ascii, im_color)


    for thread in threads:
        thread.join()

    os.system("cls")