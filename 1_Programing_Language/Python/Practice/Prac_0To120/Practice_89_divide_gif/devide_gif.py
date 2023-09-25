from PIL import Image
import os

def devide_gif(path):
    with Image.open(path) as im:
        if im.format != "GIF":
            print("Not a gif file")
            return
        jpg_list = []
        im.seek(0)
        i = 0
        while True:
            try:
                im.seek(im.tell() + 1)
                im.save(os.path.join(os.path.dirname(path), os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % i))
                jpg_list.append(os.path.join(os.path.dirname(path), os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % i))
                i += 1
            except EOFError:
                print("Done")
                break

    return jpg_list
