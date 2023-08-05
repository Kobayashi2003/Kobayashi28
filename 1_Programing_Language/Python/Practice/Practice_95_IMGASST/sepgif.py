from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import os

def gif2jpg(path, frameskip=0):
    with Image.open(path) as gif:
        if gif.format != "GIF":
            print("Not a gif file!")
            exit()

        jpg_list = []
        gif.seek(0)
        i = 0

        dir_name = os.path.splitext(os.path.basename(path))[0] + "_gif2jpg"
        dir_path = os.path.join(os.path.dirname(path), dir_name)
        
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        if frameskip == 0:
            gif.seek(gif.tell() + 1)
            gif = gif.convert("RGB")
            gif.save(os.path.join(dir_path, os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % i))
            jpg_list.append(os.path.join(dir_path, os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % i))
            return jpg_list

        while frameskip > 0:
            try:
                gif.seek(gif.tell() + frameskip)
                gif_tmp = gif.convert("RGB")
                gif_tmp.save(os.path.join(dir_path, os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % i))
                jpg_list.append(os.path.join(dir_path, os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % i))
                i += 1
            except EOFError:
                print(f"{path} is sucessfully converted to {i} jpg files")
                break

    return jpg_list
