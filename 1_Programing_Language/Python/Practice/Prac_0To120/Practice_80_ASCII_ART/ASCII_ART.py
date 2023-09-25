from PIL import Image, ImageFont, ImageDraw
import numpy as np

import glob

import os, sys
os.chdir(sys.path[0])

def ascii_srt(image_path, rate, save_flg, save_path, color, background_color, font_path, simple):

    print_in_terminal = True

    files = []
    # anlysis the path, expand the wildcards
    for path in image_path:
        for file in glob.glob(path):
            files.append(file)

    for file in files:
        # open the image
        try:
            im = Image.open(file)
        except:
            print("Can't open the file:", file)
            return

        # get the size of the terminal
        width = os.get_terminal_size().columns
        height = os.get_terminal_size().lines

        # calculate the size of the image to be generated according to the size of the terminal
        width_proportion = width / im.size[0]
        height_proportion = height / im.size[1]
        sample_rate = min(width_proportion, height_proportion) * 2
        if rate is not None and rate > 0:
            if sample_rate < rate:
                print("The rate is too large, so the image will not be displayed in the terminal.")
                print_in_terminal = False
            sample_rate = rate

        # Computer letter aspect ratio
        if font_path is None:
            font = ImageFont.truetype("SourceCodePro-Regular.ttf", size=18)
        else:
            try:
                font = ImageFont.truetype(font_path, size=18)
            except:
                print("Can't open the font file:", font_path)
                return

        aspect_ratio = font.getsize('x')[0] / font.getsize('x')[1]
        new_im_size = np.array(
            [im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]
        ).astype(int)

        # Downsample the image
        im = im.resize(new_im_size)

        # keep a copy of image for color sampling
        im_color = np.array(im)

        # Convert to gray scale image
        im = im.convert('L')

        # Convert to numpy array for image manipulation
        im = np.array(im)

        # Defines all the symbols in ascending order that will form the final ascii
        if simple:
            symbols = np.array(list(" .-v*M@#"))
        else:
            symbols = np.array(list(" `.^\\:~<!ct+{i7?u30pw4A8DX\%#HWM"))

        # Normalize the minimum and maximum to [0, max_symbol_index]
        im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

        # Generate the ascii art
        ascii = symbols[im.astype(int)]

        # Create a output image for drawing ascii text
        letter_size = font.getsize('x')
        im_out_size = new_im_size * letter_size

        # bg_color = "black"
        bg_color = background_color
        im_out = Image.new('RGB', tuple(im_out_size), bg_color)
        draw = ImageDraw.Draw(im_out)

        # Draw text
        y = 0
        for i, line in enumerate(ascii):
            for j, ch in enumerate(line):
                if color is False:
                    color = (255, 255, 255) # white
                else:
                    color = tuple(im_color[i, j]) # sample color from original image
                draw.text((j * letter_size[0], y), ch, font=font, fill=color)
            y += letter_size[1] # increase y by letter height

        # print the ascii art to the terminal with color
        if print_in_terminal:
            for i, line in enumerate(ascii):
                for j, ch in enumerate(line):
                    if color is False:
                        color = (255, 255, 255)
                    else:
                        color = tuple(im_color[i, j])
                    print("\033[38;2;{};{};{}m{}\033[0m".format(*color, ch), end="")
                print()
        else:
            im_out.show()

        # Save the image
        if save_flg:
            if save_path is None:
                # save to the same directory as the original image
                save_path = os.path.dirname(file)
            # compress the image
            # im_out.save(os.path.join(save_path, os.path.basename(file) + ".ascii.png"), optimize=True, quality=95)
            im_out.save(os.path.join(save_path, os.path.basename(file) + ".ascii.png"))



        input("\nPress Enter to continue...\n")

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

        python ascii.py [options] [image path]

    Options:

        -r --rate [float]: sample rate, default size will depend on the size of the terminal
                           [float] is the ratio of the original image size to the terminal size
                           [float] should be between 0 and 1, default is 0.5
                           [float] is needed

        -s --save [path]: save the ascii art to a file, default is the current directory
                          [path] is the path to save the ascii art, default is the current directory

        -c --color [True/False]: use color in the output, default is True
                                 [True/False] is a boolean value, default is True
                                                                                              
        -b --background [color]: background color, default is black
                                 [color] is a color name, default is black
                                 [color] can be any color name in the list below

                                        [black, white, red, green, blue, yellow, cyan, magenta, gray, grey]

                                 [color] is case insensitive
                                 [color] is needed

        -f --font [path]: use a custom font, default is SourceCodePro-Regular.ttf
                          [path] is the path to the font file, default is SourceCodePro-Regular.ttf
                          [path] is needed

        --simple: use simple ascii characters, default is False
                  in simple mode, the characters used are: " .-v*M@#"
                  in not simple mode, the characters used are: " `.^\\:~<!ct+{i7?u30pw4A8DX\%#HWM"
        
        -h --help: show help message
"""

    if len(sys.argv) == 1:
        print(help_msg)
        exit()

    state = {
        "rate": None,
        "save_flg": False,
        "save_path": None,
        "color": True,
        "background_color": "black",
        "font_path": "SourceCodePro-Regular.ttf",
        "simple": False,
    }

    image_path = []

    # parse the command line arguments
    for i in range(1, len(sys.argv)):

        if sys.argv[i] in ["-r", "--rate"]:
            try:
                state["rate"] = float(sys.argv[i + 1])
                # check if the rate is valid
                if state["rate"] <= 0 or state["rate"] > 1:
                    print("Invalid rate value, use default value")
                    state["rate"] = None
                i += 1
            except:
                print("Invalid rate value, use default value")

        elif sys.argv[i] in ["-s", "--save"]:
            state["save_flg"] = True
            try:
                # check if the path is valid
                if not os.path.isdir(sys.argv[i + 1]):
                    pass
                else:
                    state["save_path"] = sys.argv[i + 1]
                    i += 1
            except:
                pass

        elif sys.argv[i] in ["-c", "--color"]:
            try:
                state["color"] = sys.argv[i + 1]
                if state["color"] in ["False", "false"]:
                    state["color"] = False
                    i += 1   
            except:
                pass

        elif sys.argv[i] in ["-b", "--background"]:
            try:
                state["background_color"] = sys.argv[i + 1]
                if state["background_color"].lower in ["black", "white", "red", "green", "blue", "yellow", "cyan", "magenta"]:
                    state["background_color"] = state["background_color"].lower()
                    i += 1
                else:
                    print("Invalid background color")
                    exit()
            except:
                print("Invalid background color")
                exit()

        elif sys.argv[i] in ["-f", "--font_path"]:
            try:
                # check if the path is valid
                if not os.path.isfile(sys.argv[i + 1]):
                    print("Invalid font path")
                    exit()
                state["font_path"] = sys.argv[i + 1]
                i += 1
            except:
                print("Invalid font path")
                exit()

        elif sys.argv[i] in ["--simple"]:
            state["simple"] = True

        elif sys.argv[i] in ["-h", "--help"]:
            print(help_msg)
            exit()

        elif sys.argv[i][0] == "-":
            print("Invalid option: {}".format(sys.argv[i]))
            print(help_msg)
            exit()

        else:
            image_path.append(sys.argv[i])

    if len(image_path) == 0:
        print("No image path")
        print(help_msg)
        exit()
        
    ascii_srt(image_path, **state)
