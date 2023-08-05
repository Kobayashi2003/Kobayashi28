from PIL import Image, ImageFont, ImageDraw
import numpy as np

import sys, os

def draw_in_terminal(ascii, im_color) :
    # param : ("terminal", ascii, im_color)
    for i, line in enumerate(ascii):
        for j, ch in enumerate(line):
            color = im_color[i][j]
            print("\033[38;2;{};{};{}m{}\033[0m".format(*color, ch), end="")
        print()


def draw_in_image(im_out):
    # param : ("image", im_out)
    im_out.show()


def ascii_srt(image_path, save_path="false", font_path="default", 
              rate=0, simple_mode=False, printing_mode="default",
              no_color=False, background_color="default"):

    """Convert image to ASCII art.

    :param image_path (str): Path to the image file.


    :param save_path (str): Path to save the ASCII art.

                "default" : save in the same directory as the image file.
                "false" : don't save the ASCII art.

                default : "false"


    :param font_path (str): Path to the font file.

                "default" : use the SourceCodePro-Regular.ttf in the same directory as the script.

                default : "default"


    :param rate (float): The rate of the image to be generated.

                the value should be between (0, 1].

                default : 0


    :param simple_mode (bool): Use simple mode or not.

                False : use " `.^\\:~<!ct+{i7?u30pw4A8DX\%#HWM" as the characters.
                True : use " .-v*M@#" as the characters.

                default : False


    :param printing_mode (str): The printing mode of the ASCII art.

                "image" : print the ASCII art as an image.
                "terminal" : print the ASCII art in the terminal.
                "auto" : the mode will depend on the size of the ASCII art.
                "default" : "auto"

                default : "default"


    :param no_color (bool): Use color or not.

                False : use color. 
                True : the ASCII art will be printed in white.

                default : False


    :param background_color (str): The background color of the ASCII art.

                "default" : black
                "RGB=(r, g, b)" : the background color will be (r, g, b)"                          
                "color_name" : the background color will be the color name.

                default : "default"


    :returns if the printing mode == "image", return a tuple ("image", Image)
             if the printing mode is "terminal", return a tuple ("terminal", ndarray, ndarray)
    """

    # print("image_path:", image_path)

    # open the image
    try:
        im = Image.open(image_path)
    except:
        print("Can't open the file:", image_path)
        exit()

    # get the size of the terminal
    width = 0
    height = 0
    try:
        width = os.get_terminal_size().columns
        height = os.get_terminal_size().lines
    except:
        print("Can't get the size of the terminal.")
        if rate == 0:
            rate = 0.1
            printing_mode = "imgae"

    width_rate = width / im.size[0]
    height_rate = height / im.size[1]

    sample_rate = min(width_rate, height_rate) * 2

    if rate > 0 and rate <= 1:
        if printing_mode == "auto" or printing_mode == "default":
            if sample_rate < rate:
                printing_mode = "image"
            else:
                printing_mode = "terminal"
        sample_rate = rate
    else:
        if printing_mode in ["auto", "default"]:
            printing_mode = "terminal"
        else:
            printing_mode = "image"


    # Computer letter aspect ratio
    if font_path == "" or font_path == "default":
        font_path = os.path.dirname(os.path.abspath(__file__)) + "/SourceCodePro-Regular.ttf"
    
    font = None
    try:
        font = ImageFont.truetype(font_path, size=18)
    except:
        print("Can't open the font file:", font_path)
        exit()

    aspect_ratio = font.getsize('x')[0] / font.getsize('x')[1]
    new_im_size = np.array(
        [im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]
    ).astype(int)

    # Resize the image
    im = im.resize(new_im_size)

    # keep a copy of the image for color sampling
    im_color = np.array(im)

    if type(im_color[0][0]) == np.uint8:
        # it means the image is in grayscale
        im_color = np.stack([im_color, im_color, im_color], axis=2)
        # no_color = True


    if no_color:
        im_color = np.full(im_color.shape, 255)

    # Convert the image to grayscale 
    im = im.convert("L")

    # Convert to numpy array for image manipulation
    im = np.array(im)
    
    # Defines all the symbols that will be used to create the ASCII art
    symbols = np.array(list(" `.^,:~\"\\<!ct+{i7?u30pw4A8DX%#HWM"))
    if simple_mode:
        symbols = np.array(list(" .-v*M@#"))
    if not no_color:
        symbols = np.array(list("▇")) 

    # Normalize the minimum and maximum to [0, max_symbol_index]
    im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

    #  Generate the ASCII art
    ascii = symbols[im.astype(int)]

    # if the printing mode is "terminal", print the ASCII art in the terminal
    if printing_mode == "terminal":
        # draw_in_terminal(ascii, im_color)
        if save_path == "false":
            return ("terminal", ascii, im_color)

    # Create a output image for drawing ascii text
    letter_size = font.getsize('x')
    im_out_size = new_im_size * letter_size

    bg_color = "black"
    if background_color.startswith("RGB="):
        bg_color = background_color[4:].replace(" ", "").replace("(", "").replace(")", "").split(",")
        bg_color = tuple([int(i) for i in bg_color])
    elif background_color not in ["default", ""]:
        bg_color = background_color
    im_out = Image.new("RGB", tuple(im_out_size), color=bg_color)
    draw = ImageDraw.Draw(im_out)

    # Draw the ASCII art
    y = 0
    for i, line in enumerate(ascii):
        for j, ch in enumerate(line):
            color = tuple(im_color[i, j])
            draw.text((j * letter_size[0], y), ch, font=font, fill=color)
        y += letter_size[1]

    if printing_mode == "image":
        if save_path == "false":
            return ("image", im_out)

    if save_path != "false":
        if save_path in ["default", ""]:
            save_path = os.path.dirname(image_path) + "/ascii_art.txt"
        im_out.save(save_path)

    if printing_mode == "terminal":
        return ("terminal", ascii, im_color)
    return ("image", im_out)