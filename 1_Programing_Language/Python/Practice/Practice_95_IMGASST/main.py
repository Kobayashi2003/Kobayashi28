from msg import hlpMsg, verMsg
from imasst import ImageAsst, pixel_analysis, draw_in_terminal, draw_in_image, draw_img

from sepgif import gif2jpg
from sepvid import vid2jpg

from mthread import mthread, mthmngr

from threading import Thread

import keyboard

import sys, os
import glob
import re
import time

remove_flg = True
auto_resize_flg = True
print_in_one_time_flg = False

# sort_flg
# 0 : dont sort
# 1 : sort by natural keys
# 2 : sort by creation time
sort_flg = 1


def pathHandler(paths_orig):

    for i in range(len(paths_orig)):
        paths_orig[i] = paths_orig[i].replace('\\', '/')
        if paths_orig[i].endswith('/'):
            paths_orig[i] = paths_orig[i][:-1]

    paths_handled = []
    while len(paths_orig) > 0:
        paths = glob.glob(paths_orig.pop(0))
        for path in paths:
            if os.path.isdir(path):
                paths_orig.append(path + '/*')
            elif os.path.isfile(path):
                paths_handled.append(path)
            else:
                print('Error: unknown path: {}'.format(path))
                return
        
    return paths_handled


def fileClassifier(paths):
    img_paths = []
    gif_paths = []
    vid_paths = []
    for path in paths:
        if path.endswith('.gif'):
            gif_paths.append(path)
        elif path.endswith('.mp4') or path.endswith('.avi'):
            vid_paths.append(path)
        else:
            img_paths.append(path)
    return img_paths, gif_paths, vid_paths


NOSIGNAL, UP, DOWN, LEFT, RIGHT, CMD, EXIT = 0, 1, -1, 2, -2, 3, 4
signal = NOSIGNAL
press_flg = False
def keyboardMonitor(key):
    # signal = 0 : no signal
    # up arrow key : signal = 1
    # down arrow key : signal = -1
    # left arrow key : signal = 2
    # right arrow key : signal = -2
    # <:> key : signal = 3 (command mode)
    # <ESC> key : signal = 4 (exit)
    global signal, press_flg
    if key.name == 'up':
        signal = 1
    elif key.name == 'down':
        signal = -1
    elif key.name == 'left':
        signal = 2
    elif key.name == 'right':
        signal = -2
    elif key.name == ':':
        signal = 3
    elif key.name == 'esc':
        signal = 4
    
    press_flg = True
keyboard.on_press(keyboardMonitor)


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


T_width_now, T_height_now, T_width_old, T_height_old = 0, 0, 0, 0
try:
    T_width_old, T_height_old = os.get_terminal_size()
    T_width_now, T_height_now = os.get_terminal_size()
except:
    auto_resize_flg = False
    # print('Warning: terminal size cannot be detected. Auto-resize will be disabled.')
def terminal_size_monitor():
    global T_width_old, T_height_old, T_width_now, T_height_now, auto_resize_flg
    last_update_time = time.time()
    while auto_resize_flg:
        if time.time() - last_update_time > 3 and \
            (T_width_now != os.get_terminal_size()[0] or \
            T_height_now != os.get_terminal_size()[1]):
            T_width_now, T_height_now = os.get_terminal_size()
            last_update_time = time.time()
            # print('Terminal size changed: {} x {}'.format(T_width_now, T_height_now))
    # print('Terminal size monitor stopped.')


def main():

    global NOSIGNAL, UP, DOWN, LEFT, RIGHT, CMD, EXIT, signal, press_flg
    global T_width_now, T_height_now, T_width_old, T_height_old, auto_resize_flg
    global remove_flg, print_in_one_time_flg, sort_flg

    ### check arguments ###
    if len(sys.argv) == 1:
        print(hlpMsg)
        return

    img = ImageAsst()
    frameskip = 0
    paths_list = []

    i = 1
    while i < len(sys.argv):

        if sys.argv[i] in ['-h', '--help']:
            print(hlpMsg)
            return
        elif sys.argv[i] in ['-v', '--version']:
            print(verMsg)
            return 

        elif sys.argv[i].startswith('-r=') or \
             sys.argv[i].startswith('--rate='):
            img.rate = sys.argv[i].split('=')[1]
            try:
                img.rate = float(img.rate)
                if img.rate <= 0 or img.rate > 1:
                    print('Error: invalid rate: {}'.format(img.rate))
                    return
            except:
                print('Error: invalid rate: {}'.format(img.rate))
                return

        elif sys.argv[i].startswith('-s') or \
             sys.argv[i].startswith('--save'):
            img.save_flg = True
            if sys.argv[i].startswith('-s=') or \
                sys.argv[i].startswith('--save='):
                img.save_path = sys.argv[i].split('=')[1]
                if not os.path.isdir(img.save_path):
                    print('Error: invalid save path: {}'.format(img.save_path))
                    return

        elif sys.argv[i] in ['-nc', '--no-color']:
            img.color_flg = False
        
        elif sys.argv[i].startswith('--bc=') or \
             sys.argv[i].startswith('--background-color='):
             img.bg_color = sys.argv[i].split('=')[1]

        elif sys.argv[i] in ['--ascii']:
            img.ascii_mode = True

        elif sys.argv[i].startswith('-p=') or \
             sys.argv[i].startswith('--print='):
            img.print_mode = sys.argv[i].split('=')[1]
            if img.print_mode not in ['image', 'terminal', 'auto']:
                print('Error: invalid print mode: {}'.format(img.print_mode))
                return

        elif sys.argv[i].startswith('--fs=') or \
             sys.argv[i].startswith('--frameskip='):
            frameskip = sys.argv[i].split('=')[1]
            try:
                frameskip = int(frameskip)
                if frameskip < 0:
                    print('Error: invalid frameskip: {}'.format(frameskip))
                    return
            except:
                print('Error: invalid frameskip: {}'.format(frameskip))
                return

        elif sys.argv[i].startswith('-'):
            print('Error: unknown option: {}'.format(sys.argv[i]))
            return

        else:
            paths_list.append(sys.argv[i])

        i += 1

    if len(paths_list) == 0:
        print('Error: no image path is set')
        return
    paths_list = pathHandler(paths_list)

    img_paths, gif_paths, vid_paths = fileClassifier(paths_list)

    for path in gif_paths:
        g2j_list = gif2jpg(path, frameskip)
        img_paths.extend(g2j_list)

    for path in vid_paths:
        v2j_list = vid2jpg(path, frameskip)
        img_paths.extend(v2j_list)

    if len(img_paths) == 0:
        print('Error: no image file is found')
        return


    ### start processing ###
    mythread_manager = mthmngr()
    mythread_manager.start()

    index = []
    for path in img_paths:
        img.img_path = path
        img_tmp = ImageAsst().copy_constructor(img)
        filename = os.path.basename(path).split('.')[0]
        index.append(filename)
        mythread_manager.create_mthread(pixel_analysis, filename, img_tmp)
    results = [None for i in range(len(index))]


    if sort_flg == 1:
        index.sort(key=natural_keys)
        for i in range(len(index)):
            print('pretreatment: {}'.format(index[i]))
    elif sort_flg == 2:
        index.sort(key=lambda x: os.path.getctime(x))
        for i in range(len(index)):
            print('pretreatment: {}'.format(index[i]))


    if print_in_one_time_flg:
        while None in results:
            for i in range(len(results)):
                if results[i] is None:
                    results[i] = mythread_manager.get_result(index[i])
                    if results[i] is not None:
                        print('finished: {}'.format(index[i]))
                        break
        for r in results:
            if r[0] == 'image':
                draw_in_image(r[1])
            elif r[0] == 'terminal':
                draw_in_terminal(r[1], r[2])
                print()
        mythread_manager.stop()
        return
        

    if auto_resize_flg:
        t_terminal_size_monitor = Thread(target=terminal_size_monitor)
        t_terminal_size_monitor.start()


    MAX_PAGE = len(index) 
    page = 0
    update_flg = True
    msg_flg = True
    while signal != EXIT:

        if auto_resize_flg:
            if T_width_old != T_width_now or T_height_old != T_height_now:
                T_width_old, T_height_old = T_width_now, T_height_now
                mythread_manager.restart_all_threads()
                update_flg = True

        if press_flg:

            if signal == UP:
                if page > 0:
                    page -= 1
                    update_flg, msg_flg = True, True
            elif signal == DOWN:
                if page < MAX_PAGE - 1:
                    page += 1
                    update_flg, msg_flg = True, True
            elif signal == LEFT:
                filename = index[page]
                try:
                    filenum = int(filename.split('_')[-1])
                    filenum -= 1
                    filename = '_'.join(filename.split('_')[:-1]) + '_' + str(filenum)
                    if filename in index:
                        page = index.index(filename)
                        update_flg, msg_flg = True, True
                except:
                    pass
            elif signal == RIGHT:
                filename = index[page]
                try:
                    filenum = int(filename.split('_')[-1])
                    filenum += 1
                    filename = '_'.join(filename.split('_')[:-1]) + '_' + str(filenum)
                    if filename in index:
                        page = index.index(filename)
                        update_flg, msg_flg = True, True
                except:
                    pass                

            elif signal == CMD:
                cmd = input()
                if cmd == ':q':
                    break 
                elif cmd.startswith(':g'):
                    try:
                        page = int(cmd.split(' ')[1]) - 1
                        if page < 0 or page >= MAX_PAGE:
                            raise ValueError
                        update_flg, msg_flg = True, True
                    except:
                        print('Error: invalid page number')
                elif cmd == ':r':
                    mythread_manager.restart_thread(index[page])
                    update_flg, msg_flg = True, True
                elif cmd == ':ra':
                    mythread_manager.restart_all_threads()
                    update_flg, msg_flg = True, True
                else:
                    print('Error: invalid command')

            elif signal == EXIT:
                break

            signal = NOSIGNAL
            press_flg = False

        if update_flg:
            if msg_flg:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('[page: {}/{}]'.format(page+1, MAX_PAGE))

            if results[page] is None:
                status = mythread_manager.check_thread_status(id=index[page])
                if status == 'running':
                    if msg_flg:
                        print('processing...')
                elif status == 'finished':
                    result = mythread_manager.get_result(index[page])
                    if result is None:
                        print('Error: cannot get the img data')
                    else:
                        draw_img(result)
                    print(' [{}/{}]'.format(page+1, MAX_PAGE))
                    update_flg = False
                elif status == 'waiting':
                    if msg_flg:
                        print('waiting...')
                    mythread_manager.prioty_thread(index[page])
            else:
                draw_img(results[page])
                print(' [{}/{}]'.format(page+1, MAX_PAGE))
                update_flg = False
            msg_flg = False
    
    if auto_resize_flg:
        auto_resize_flg = False
        t_terminal_size_monitor.join()
    mythread_manager.stop()


    # remove the temporary files (the directory end with '_gif2jpg' or '_vid2jpg')        
    if remove_flg:

        for path in gif_paths:
            dirname = os.path.splitext(os.path.basename(path))[0]
            dir = os.path.dirname(path) + '/' + dirname + '_gif2jpg'
            for file in os.listdir(dir):
                os.remove(dir + '/' + file)
            os.rmdir(dir)
            
        for path in vid_paths:
            dirname = os.path.splitext(os.path.basename(path))[0]
            dir = os.path.dirname(path) + '/' + dirname + '_vid2jpg'
            for file in os.listdir(dir):
                os.remove(dir + '/' + file)
            os.rmdir(dir)

    print('Done')
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
if __name__ == '__main__':
    main()