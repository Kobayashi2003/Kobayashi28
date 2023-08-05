import cv2
import os

# 2023/2/24 BUG: 无法正常读取视频文件

def vid2jpg(path, frameskip=0):
    cam = cv2.VideoCapture(path)
    if not cam.isOpened():
        print('Error: Not a video file!')
        exit()

    jpg_list = []
    count = 0

    dir_name = os.path.splitext(os.path.basename(path))[0] + "_vid2jpg"
    dir_path = os.path.join(os.path.dirname(path), dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
    if frameskip == 0:
        ret, frame = cam.read()
        cv2.imwrite(os.path.join(dir_path, os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % count), frame)
        jpg_list.append(os.path.join(dir_path, os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % count))
        return jpg_list
    
    i = 0
    while frameskip > 0:
        ret, frame = cam.read()
        if ret == False:
            print("Done")
            break
        if i % frameskip == 0:
            cv2.imwrite(os.path.join(dir_path, os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % count), frame)
            jpg_list.append(os.path.join(dir_path, os.path.splitext(os.path.basename(path))[0] + "_%d.jpg" % count))
            count += 1
        i += 1
    
    print(f"{path} is sucessfully converted to {count} jpg files")
    cam.release()
    cv2.destroyAllWindows()

    return jpg_list