from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os

class ImageAsst:

    def __init__(self):
        self.rate = 0
        self.save_flg = False
        self.save_path = ""
        self.color_flg = True
        self.bg_color = 'black'
        self.ascii_mode = False
        self.print_mode = 'auto'

        self.img_path = ""

        self.img_result = None

    def copy_constructor(self, image):
        try:
            self.rate = image.rate
            self.save_flg = image.save_flg
            self.save_path = image.save_path
            self.color_flg = image.color_flg
            self.bg_color = image.bg_color
            self.ascii_mode = image.ascii_mode
            self.print_mode = image.print_mode

            self.img_path = image.img_path
            return self
        except:
            print('Error: invalid image')
            return None

    def set_img_path(self, img_path):
        if not self.check_img_path(img_path):
            return
        self.img_path = img_path

    def check_img_path(self, img_path):
        if not os.path.isfile(img_path):
            print('Error: invalid image path: {}'.format(img_path))
            return False
        return True

    def get_img(self, img_path):
        if not self.check_img_path(img_path):
            return None
        return Image.open(img_path)

    def get_save_path(self):
        if self.save_flg:
            file_name = os.path.basename(self.img_path).split('.')[0] + 'imgasst.png'
            if self.save_path == "":
                dir_path = os.path.dirname(self.img_path)
                return os.path.join(dir_path, file_name)
            else:
                return os.path.join(self.save_path, file_name)    
        else:
            return None

    def create_img(self):
        self.img_result = pixel_analysis(self)

    def print_img(self):
        if self.img_result is None:
            print('Error: image is not created')
            return

        if self.img_result[0] == 'terminal':
            draw_in_terminal(self.img_result[1], self.img_result[2])
        elif self.img_result[0] == 'image':
            draw_in_image(self.img_result[1])
            
def draw_img(result):
    os.system('cls' if os.name == 'nt' else 'clear')
    if result[0] == 'terminal':
        draw_in_terminal(result[1], result[2])
    elif result[0] == 'image':
        draw_in_image(result[1])

def draw_in_terminal(char_table, im_color):
    for i, line in enumerate(char_table):
        for j, ch in enumerate(line):
            color = im_color[i][j]
            print("\033[38;2;{};{};{}m{}\033[0m".format(*color, ch), end="")
        if i != len(char_table) - 1:
            print()


def draw_in_image(im_out):
    im_out.show()


def pixel_analysis(image):
    # :param image: imasst.ImageAsst
    IM = ImageAsst().copy_constructor(image)
    im = IM.get_img(IM.img_path)

    # get font and font size
    font_path = os.path.dirname(os.path.abspath(__file__)) + '/SourceCodePro-Regular.ttf'
    font = None
    try:
        font = ImageFont.truetype(font_path, size=18)
    except:
        print('Error: can not open the font file: {}'.format(font_path))
        exit()
    if IM.ascii_mode:
        aspect_ratio = font.getsize('x')[0] / font.getsize('x')[1]
    else:
        aspect_ratio = font.getsize('▇')[0] / font.getsize('▇')[1]

    # get terminal size
    width, height = 0, 0
    try:
        width, height = os.get_terminal_size().columns, os.get_terminal_size().lines
    except:
        print('Error: can not get terminal size')
        if IM.rate <= 0 or IM.rate > 1:
            exit()

    width_rate = width / im.size[0]
    height_rate = height / (im.size[1] * aspect_ratio)
    sample_rate = min(width_rate, height_rate)

    if IM.rate > 0 and IM.rate <= 1:
        if IM.print_mode == 'auto':
            if sample_rate < IM.rate:
                IM.print_mode = 'image'
            else:
                IM.print_mode = 'terminal'
        sample_rate = IM.rate
    else:
        if IM.print_mode == 'auto':
            IM.print_mode = 'terminal'

    # resize image
    new_im_size = np.array([im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]).astype(int)
    im = im.resize(new_im_size)

    im_color = np.array(im)
    if type(im_color[0, 0]) is np.uint8:
        im_color = np.stack((im_color, im_color, im_color), axis=2)
    if not IM.color_flg:
        im_color = np.full(im_color.shape, 255)

    # convert image to gray scale
    im = im.convert('L')
    im = np.array(im)

    # symbol list
    symbols = np.array(list("▇")) 
    if IM.ascii_mode:
        symbols = np.array(list(" `.^,:~\"\\<!ct+{i7?u30pw4A8DX%#HWM"))
    if im.min() == im.max():
        # a image with only one color
        im = np.full(im.shape, symbols.size - 1)
    else:
        im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

    # create new image
    char_table = symbols[im.astype(int)]

    if IM.print_mode == "terminal":
        if not IM.save_flg:
            return ("terminal", char_table, im_color)

    # create a output image
    letter_size = font.getsize('▇')
    if IM.ascii_mode:
        letter_size = font.getsize('x')
    im_out_size = new_im_size * letter_size
    bg_color = IM.bg_color
    im_out = Image.new('RGB', im_out_size, color=bg_color)
    draw = ImageDraw.Draw(im_out)

    # draw image
    y = 0
    for i, line in enumerate(char_table):
        for j, ch in enumerate(line):
            color = tuple(im_color[i, j])
            draw.text((j * letter_size[0], y), ch, font=font, fill=color)
        y += letter_size[1]

    if IM.print_mode == "image":
        if not IM.save_flg:
            return ("image", im_out)

    if IM.save_flg:
        save_path = IM.get_save_path()
        im_out.save(save_path)
        print('Image saved: {}'.format(save_path))    

    if IM.print_mode == "terminal":
        return ("terminal", char_table, im_color)
    elif IM.print_mode == "image":
        return ("image", im_out)
