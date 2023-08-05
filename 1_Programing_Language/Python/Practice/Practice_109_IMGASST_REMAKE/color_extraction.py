from PIL import Image, ImageFont, ImageSequence
import numpy as np

from common import DEFAULT_FONT_PATH, DEFAULT_FONT_SIZE, MAX_WORKERS, SUPPORTED_IMAGE_FORMAT, SUPPORTED_IMAGE_FORMAT_SEQUENCE, ERROR_RATE, Result, Status


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
        import magic
        try:
            fmt = str.lower(magic.from_buffer(im.tobytes(), mime=True).split('/')[1])
        except:
            error_msg = 'Error: invalid image file: {}'.format(imgfile)
            return Result(Status.error, error_msg)
        else:
            im.format = fmt
    fmt = str.lower(fmt)

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
        import magic
        try:
            fmt = str.lower(magic.from_buffer(im.tobytes(), mime=True).split('/')[1])
        except:
            error_msg = 'Error: invalid image file: {}'.format(imgfile)
            return Result(Status.error, error_msg)
        else:
            im.format = fmt
    fmt = str.lower(fmt)

    duration = im.info['duration']

    from concurrent import futures
    workers = min(MAX_WORKERS, im.n_frames)
    results = [None for _ in range(im.n_frames)]
    error_frames = []
    with futures.ThreadPoolExecutor(workers) as executor:
        to_do = []
        try:
            while True:
                try:
                    to_do.append(executor.submit(color_extraction_one, im.copy(), *args, **kwargs))
                    log_msg = 'Scheduled for {}: {!r}'.format(im.tell(), to_do[-1])
                except:
                    to_do.append(None)
                im.seek(im.tell() + 1)
        except EOFError: 
            pass

        for frame, future in enumerate(to_do):
            if future is None:
                results[frame] = Result(Status.error, None)
            else:
                try:
                    res = future.result()
                except:
                    results[frame] = Result(Status.error, None)
                else:
                    results[frame] = res
 
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
        import magic
        try:
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


if __name__ == '__main__':

    MAX_WIDTH = 1e5
    MAX_HEIGHT = 1e5

    import os

    env = os.environ
    columns, lines = os.get_terminal_size()
    print(f"terminal size: columns: {columns}, lines: {lines}")

    # default size
    size = None

    # fit terminal size 
    size = (columns, lines)

    # fit terminal height
    # size = (MAX_WIDTH, lines)

    # fit terminal width
    # size = (columns, MAX_HEIGHT)

    aspect_ratio = 0.33
    if columns > 1e3:
        # aspect_ratio = 1.5 # when use Hack NF in size 2
        # aspect_ratio = 2.0 # when use Hack NF in size 1
        pass

    # create a 1000x1000 image with white background
    # from PIL import Image, ImageDraw
    # im = Image.new('RGB', (1000, 1000), (255, 255, 255))
    # res = color_extraction(im, size=size, mode='RGB', aspect_ratio=aspect_ratio)
    # print_img(res, frame_size=os.get_terminal_size(), pos=(0, 0))
    # input()

    # exit()
    import Buffers
    import time
    from colors2str import data_preprocess_one, data_preprocess_seq
    buffer = Buffers.Buffers(5)
    time_log = []
    with open('./88.gif', 'rb') as f:
        res = color_extraction_sequence(f, size=size, mode='RGB', aspect_ratio=aspect_ratio)
        duration = res.data[1]
        if res is None or res.status == Status.error:
            exit()
            
        output_seq = data_preprocess_seq(res, frame_size=os.get_terminal_size(), pos=(-10, -10))
    import sys
    from itertools import cycle
    for output in cycle(output_seq):
        buffer.switch()
        buffer.write(output)
        buffer.flush()
        time.sleep(duration / 1000)



        # move = 50
        # for i in range(move):
        #     t_start = time.perf_counter()
        #     output = data_preprocess_one(res, frame_size=os.get_terminal_size(), pos=(i, i))
        #     t_stop = time.perf_counter()
        #     time_log.append(("data perprocess" , i, t_stop - t_start))

        #     t_start = time.perf_counter()
        #     buffer.switch()
        #     buffer.write(output)
        #     buffer.flush()
        #     t_stop = time.perf_counter()
        #     time_log.append(("buffer write" , i, t_stop - t_start))

        #     time.sleep(0.1)

        # for i in range(2*move):
        #     t_start = time.perf_counter()
        #     output = data_preprocess_one(res, frame_size=os.get_terminal_size(), pos=(move-i, move-i))
        #     t_stop = time.perf_counter()
        #     time_log.append(("data perprocess" , move-i, t_stop - t_start))

        #     t_start = time.perf_counter()
        #     buffer.switch()
        #     buffer.write(output)
        #     buffer.flush()
        #     t_stop = time.perf_counter()
        #     time_log.append(("buffer write" , move - i, t_stop - t_start))

        #     time.sleep(0.1)


    exit()

    with open('./image.jpg', 'rb') as f:
        res = color_extraction(f, size=size, mode='L', aspect_ratio=aspect_ratio)
        if res is None or res.status == Status.error:
            exit()
        print_img(res, frame_size=os.get_terminal_size(), pos=(0, 0))
        input()
        import time
        move = 500
        # for i in range(move):
        #     print_img(res, frame_size=os.get_terminal_size(), pos=(i, i))
        #     time.sleep(0.1)
        for i in range(2*move):
            print_img(res, frame_size=os.get_terminal_size(), pos=(move-i, move-i))
            time.sleep(0.1)

    exit()

    import time

    t1_start = time.perf_counter()
    with open('./image_gif.gif', 'rb') as f:
        res = color_extraction_sequence(f, size=size, mode='RGB', aspect_ratio=aspect_ratio)
        if res is None or res.status == Status.error:
            exit()
        fmt, duration, results = res.data 
        l = len(results)
    t1_stop = time.perf_counter()
    print("t1 time: {}".format(t1_stop - t1_start))

    import io
    output_list = []
    for frame, result in enumerate(results):
        fmt, width, height, mode, colors = result.data
        # print the color by ansi escape code as background color
        output = io.StringIO()
        for row in colors:
            for i, color in enumerate(row):
                if i >= columns // 2:
                    break
                output.write("\033[48;2;{};{};{}m  \033[0m".format(*color))
            output.write('\n')
        output.write('frame: {}/{}'.format(frame % l + 1, l))
        output_list.append(output.getvalue()) 

    import itertools
    import Buffers

    buffer = Buffers.Buffers(5)
    while True:
        for frame, output in enumerate(itertools.cycle(output_list)):
            buffer.switch()
            buffer.print(output, end='')
            buffer.flash()
            time.sleep(duration / 1000)

    exit()

    import itertools 
    while True:
        for frame, result in enumerate(itertools.cycle(results)):
            fmt, width, height, mode, colors = result
            # print the color by ansi escape code as background color
            import io
            import Buffers
            buffer = Buffers.Buffers(5)
            output = io.StringIO()
            for row in colors:
                for i, color in enumerate(row):
                    if i >= columns // 2:
                        break
                    output.write("\033[48;2;{};{};{}m  \033[0m".format(*color))
                output.write('\n')
            output.write('frame: {}/{}'.format(frame % l + 1, l))
            content = output.getvalue()
            buffer.switch()
            buffer.print(content, end='')
            buffer.flash()
            time.sleep(duration / 1000)

    exit()

    t1_start = time.perf_counter()
    with open('./image2.jpg', 'rb') as f:
        # im = Image.open(f)
        result = color_extraction(f, size=size, mode='RGB', aspect_ratio=aspect_ratio)
        if result is None:
            exit()
        fmt, width, height, mode, colors = result
    t1_stop = time.perf_counter()
    print("t1 time: {}".format(t1_stop - t1_start))
    

    t2 = time.perf_counter()
    # print the color by ansi escape code as background color
    import io
    import Buffers
    buffer = Buffers.Buffers(5)
    output = io.StringIO()
    for row in colors:
        for i, color in enumerate(row):
            if i >= columns // 2:
                break
            output.write("\033[48;2;{};{};{}m  \033[0m".format(*color))
        output.write('\n')
    t2_stop = time.perf_counter()
    content = output.getvalue()
    print("t2 time: {}".format(t2_stop - t2))

    t3_start = time.perf_counter()
    # dont use print() to print the color, it's too slow
    import win32console
    win32console.SetConsoleTitle('color_extraction')
    buffer.switch()
    buffer.print(content, end='')
    buffer.flash()
    t3_stop = time.perf_counter()
    print("t3 time: {}".format(t3_stop - t3_start))

    input()

    exit()

    import Buffers
    
    t2_start = time.perf_counter()
    buffer = Buffers.Buffers(5)
    buffer.switch()
    for row in colors:
        for i, color in enumerate(row):
            if i >= columns // 2:
                break
            buffer.print("\033[48;2;{};{};{}m  \033[0m".format(*color), end='')
        buffer.print()
    buffer.flash()
    t2_stop = time.perf_counter()
    print("t2 time: {}".format(t2_stop - t2_start))
    
    exit()

    t2_start = time.perf_counter()
    import sys
    for row in colors:
        for i, color in enumerate(row):
            if i >= columns // 2:
                break
            sys.stdout.write("\033[48;2;{};{};{}m  \033[0m".format(*color))
        sys.stdout.write('\n')
    t2_stop = time.perf_counter()
    print("t2 time: {}".format(t2_stop - t2_start))