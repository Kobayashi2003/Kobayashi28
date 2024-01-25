from PIL import Image, ImageFont, ImageSequence
import numpy as np

from common import Result, Status
from common import DEFAULT_FONT_PATH, DEFAULT_FONT_SIZE
from common import MAX_WORKERS, MAX_WAITING_TIME, ERROR_RATE
from common import SUPPORTED_IMAGE_FORMAT, SUPPORTED_IMAGE_FORMAT_SEQUENCE


def color_extraction_one(imgfile, size=None, mode='RGB', *args,
                         font_path=DEFAULT_FONT_PATH,
                         font_size=DEFAULT_FONT_SIZE,
                         aspect_ratio=None, **kwargs):
    """This function is mainly used to extract color attributes from an image file under the a given font, border size limit, and image mode. The extracted color attributes are stored in a numpy array.

    Args:
        imgfile (Image | BytesIO): The image file to be extracted. If it is a BytesIO object, it will be opened by Image.open() first. If it is an Image object, it will be used directly.
        size (tuple(frame_width, frame_height), optional): The size of the frame to be fitted. If it is None, the original size of the image will be used. Defaults to None.
        mode (str, optional): The image mode to be converted. Defaults to 'RGB'.
        font_path (_type_, optional): The path of the font file to be used. Defaults to DEFAULT_FONT_PATH.
        font_size (int, optional): The font size to be used. Defaults to DEFAULT_FONT_SIZE.
        aspect_ratio (float, optional): The aspect ratio of the font to be used (font-width / font-height). If it is None, the aspect ratio of the font will be calculated automatically. Defaults to None. Once it is set, the font path and font size will be ignored.
    Returns:
        Result(Status.done, (fmt, width, height, mode, colors)) | Result(Status.error, error_msg)
    """

    # open the image from a bufferreader, and get the image information
    try:
        im = Image.open(imgfile)
    except:
        im = imgfile
    assert isinstance(im, Image.Image), 'Error: invalid image file: {}'.format(imgfile)

    fmt, width, height = im.format, im.width, im.height

    if fmt is None:
        try:
            import magic
            fmt = str.lower(magic.from_buffer(im.tobytes(), mime=True).split('/')[1])
        except:
            error_msg = 'Error: invalid image file: {}'.format(imgfile)
            # return Result(Status.error, error_msg)
        finally:
            im.format = fmt

    original_img_info = '[original image]: fmt: {}, width: {}, height: {}'.format(fmt, width, height)

    if aspect_ratio is None:
        # get the font information
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            error_msg = 'Error: can not open the font file: {}'.format(font_path)
            status = Status.error
            return Result(status, error_msg)
        string = '█'
        bbox = font.getmask(string).getbbox()
        font_width, font_height = font.getlength(string*2) - font.getlength(string), bbox[3] - bbox[1]
        aspect_ratio = font_width / font_height
        font_info = '[font]: path: {}, size: {}'.format(font_path, font_size)
    aspect_ratio_info = '[aspect_ratio]: {}'.format(aspect_ratio)
    # calculate the actual width and height of the image printed in this font
    # then resize the image to the corrent aspect ratio
    actual_width, actual_height = width, int(height * aspect_ratio)
    im = im.resize((actual_width, actual_height))
    width, height = im.width, im.height
    actual_img_info = '[actual image]: fmt: {}, width: {}, height: {}'.format(fmt, width, height)
    # create the thumbnail to fit the frame size
    if size is None:
        size = (width, height)
    try:
        frame_width, frame_height = size
        int(frame_width), int(frame_height)
    except:
        error_msg = 'Error: invalid size: {}'.format(size)
        return Result(Status.error, error_msg)
    im.thumbnail(size)
    width, height = im.width, im.height
    final_img_info = '[final image]: fmt: {}, width: {}, height: {}'.format(fmt, im.width, im.height)

    # convert the image mode
    if im.mode != mode:
        try:
            im = im.convert(mode)
        except:
            error_msg = 'Error: invalid image mode: {}'.format(mode)
            return Result(Status.error, error_msg)
        else:
            convert_info = 'convert image mode: {} -> {}'.format(im.mode, mode)

    # get the color information
    colors = np.array(im)
    colors_info = '[colors]: shape: {}, dtype: {}'.format(colors.shape, colors.dtype)

    return Result(Status.done, (fmt, width, height, mode, colors))


def color_extraction_sequence(imgfile, *args, **kwargs):
    """This function is used to extract color attributes from each frame of an sequence image,
    and return a list of color attributes. The arguments will be passed to color_extraction().

    Returns:
        Result(Status.done, (duration, results)) | Result(Status.error, error_msg)
    """

    try:
        im = Image.open(imgfile)
    except:
        im = imgfile
    assert isinstance(im, Image.Image), 'Error: invalid image file: {}'.format(imgfile)

    fmt = im.format
    if fmt is None:
        try:
            import magic
            fmt = str.lower(magic.from_buffer(im.tobytes(), mime=True).split('/')[1])
        except:
            error_msg = 'Error: invalid image file: {}'.format(imgfile)
            return Result(Status.error, error_msg)
        finally:
            im.format = fmt
    fmt = str.lower(fmt)

    duration = im.info['duration']

    from concurrent import futures
    from asyncio import InvalidStateError
    from time import sleep
    workers = min(MAX_WORKERS, im.n_frames)
    results = [None for _ in range(im.n_frames)]
    error_frames = []
    with futures.ThreadPoolExecutor(workers) as executor:
        to_do = []
        try:
            while True:
                try:
                    im_copy = im.copy()
                    im.fmt, im.duration = fmt, duration
                    to_do.append(executor.submit(color_extraction_one, im_copy, *args, **kwargs))
                    log_msg = 'Scheduled for {}: {!r}'.format(im.tell(), to_do[-1])
                except:
                    to_do.append(None)
                im.seek(im.tell() + 1)
        except EOFError:
            pass

        for frame, future in enumerate(to_do):
            if future is None:
                error_msg = 'Error: future task is None: {}'.format(frame)
                results[frame] = Result(Status.error, error_msg)
            else:
                wait_time = 0
                while True:
                    try:
                        res = future.result()
                    except InvalidStateError:
                        sleep(0.1)
                        wait_time += 0.1
                        if wait_time > MAX_WAITING_TIME:
                            error_msg = 'Error: waiting time out: {}'.format(frame)
                            results[frame] = Result(Status.error, error_msg)
                            break
                    except:
                        error_msg = 'Error: unknown error: {}'.format(frame)
                        results[frame] = Result(Status.error, error_msg)
                        break
                    else:
                        results[frame] = res
                        break

    for i, result in enumerate(results):
        if result.status == Status.error:
            error_frames.append(i)
            if len(error_frames) > ERROR_RATE * len(results):
                error_msg = 'Error: more than half of the frames are not extracted successfully: {}'.format(error_frames)
                return Result(Status.error, error_msg)
            results[i] = Result(Status.done, ('error', 0, 0, 'RGB', np.zeros((1, 1, 3), dtype=np.uint8)))

    return Result(Status.done, (fmt, duration, results))


def color_extraction(imgfile, *args, **kwargs):
    try:
        im = Image.open(imgfile)
    except:
        im = imgfile
    assert isinstance(im, Image.Image), 'Error: invalid image file: {}'.format(imgfile)

    fmt = im.format
    if fmt is None:
        try:
            import magic
            fmt = str.lower(magic.from_buffer(im.tobytes(), mime=True).split('/')[1])
        except:
            error_msg = 'Error: invalid image file: {}'.format(imgfile)
            return Result(Status.error, error_msg)
        else:
            im.format = fmt
    fmt = str.lower(fmt)

    if fmt in SUPPORTED_IMAGE_FORMAT:
        return color_extraction_one(im, *args, **kwargs)
    elif fmt in SUPPORTED_IMAGE_FORMAT_SEQUENCE:
        return color_extraction_sequence(im, *args, **kwargs)
    else:
        error_msg = 'Error: unsupported image format: {}'.format(fmt)
        return Result(Status.error, error_msg)


def simple_main_loop():

    import os
    import re
    import time
    import random
    import msvcrt
    import Buffers
    from colors2str import colors2str
    from analysis_path import fd_files
    from analysis_path import NAME_FILTER, PATH_FILTER, SIZE_FILTER, NATURAL_SORT
    from common import get_proc_args, get_terminal_size
    from common import MAX_DEPTH
    from common import ADVANCED_MODE_CODE, SIMPLE_MODE_CODE, TEST_MODE_CODE

    MAX_WIDTH = 1e5
    MAX_HEIGHT = 1e5

    proc_args = get_proc_args()
    args_path = proc_args.path
    args_fit  = proc_args.fit
    args_mode = proc_args.mode
    args_aspect_ratio = proc_args.aspect_ratio

    buffer = Buffers.Buffers()
    columns, lines = get_terminal_size()
    restart_flg = False
    change_proc_mode = False
    change_test_mode = False

    # frame size
    fit = args_fit if args_fit is not None else 3
    size = (columns if fit & 2 else MAX_WIDTH, lines if fit & 1 else MAX_HEIGHT)
    # aspect ratio
    aspect_ratio = args_aspect_ratio if args_aspect_ratio is not None else 0.33
    # image mode
    mode_list = [ 'RGB', 'L', 'P' ]
    mode = args_mode if args_mode in mode_list else 'RGB'
    # image path
    work_dir = os.path.abspath(args_path) if args_path is not None else os.getcwd()
    img_list = fd_files(work_dir, depth=MAX_DEPTH, filter=(NAME_FILTER(r'.*\.(jpg|jpeg|png|bmp|ico|tiff?)$') & PATH_FILTER(r'.*') & SIZE_FILTER(0, 1e10)), sorter=NATURAL_SORT())

    pos = (0, 0)

    update_flg = True
    redo_flg   = True
    cur_idx    = 0
    im = Image.open(img_list[cur_idx])
    while 1:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in b'q\x1b':
                break
            elif ch in b'w':
                pos = (pos[0], pos[1]-max(1, lines//100))
            elif ch in b's':
                pos = (pos[0], pos[1]+max(1, lines//100))
            elif ch in b'a':
                pos = (pos[0]-max(1, columns//100), pos[1])
            elif ch in b'd':
                pos = (pos[0]+max(1, columns//100), pos[1])
            elif ch in b'W':
                pos = (pos[0], pos[1]-max(1, lines//20))
            elif ch in b'S':
                pos = (pos[0], pos[1]+max(1, lines//20))
            elif ch in b'A':
                pos = (pos[0]-max(1, columns//20), pos[1])
            elif ch in b'D':
                pos = (pos[0]+max(1, columns//20), pos[1])
            elif ch in b'r':
                pos = (0, 0)
            elif ch in b'h':
                cur_idx = (cur_idx - 1) % len(img_list)
                im = Image.open(img_list[cur_idx])
            elif ch in b'l':
                cur_idx = (cur_idx + 1) % len(img_list)
                im = Image.open(img_list[cur_idx])
            elif ch in b'm':
                mode = mode_list[(mode_list.index(mode) + 1) % len(mode_list)]
            elif ch in b'j':
                aspect_ratio -= 0.01
            elif ch in b'k':
                aspect_ratio += 0.01
            elif ch in b'J':
                aspect_ratio -= 0.1
            elif ch in b'K':
                aspect_ratio += 0.1
            elif ch in b'R':
                restart_flg = True
                break
            elif ch in b'C':
                change_proc_mode = True
                break
            elif ch in b'T':
                change_test_mode = True
                break
            else:
                pass
            aspect_ratio = max(0.01, min(3, aspect_ratio))

            update_flg = True
            if ch in b'RmjkJKhl':
                redo_flg = True

            while msvcrt.kbhit():
                msvcrt.getch()

        if redo_flg:
            redo_flg = False
            res = color_extraction(im, size=size, mode=mode, aspect_ratio=aspect_ratio)
        if update_flg:
            buffer.switch()
            buffer.write(colors2str(res, frame_size=(columns, lines), pos=pos))
            buffer.write('pos: {}\nmode: {}\n'.format(pos, mode) + 'aspect_ratio: %0.2f\n' % aspect_ratio)
            buffer.flush()
            update_flg = False
        time.sleep(0.01)

    if restart_flg:
        return SIMPLE_MODE_CODE
    if change_proc_mode:
        return ADVANCED_MODE_CODE
    if change_test_mode:
        return TEST_MODE_CODE
    return 0

if __name__ == '__main__':
    while simple_main_loop():
        pass