import numpy as np
import time
from PIL import Image, ImageGrab


def create_white_img():
    # create a white image
    img = Image.new('RGB', (1920, 1080), color='white')
    img.save('white.png')


def check_white_screen():
    # check if the screen is white

    img = ImageGrab.grab()
    img_rgb = img.convert('RGB')
    rgb_array = np.array(img_rgb)
    white = np.array([255, 255, 255])

    count = sum(sum(sum(white - rgb_array < 10))) / 3
    if count >= 1920 * 1080 * 0.9:
        return True 
    return False

    
if __name__ == '__main__':
    while not check_white_screen():
        print('not white screen')
        time.sleep(0.05)
    print('white screen')
    import os 
    os.startfile('genshen.mp4') # for simplicity, here I use a mp4 file
