from functools import lru_cache

from common import Result, Status
from common import MAX_WORKERS, MAX_LOAD_NUM
from common import SUPPORTED_IMAGE_FORMAT, SUPPORTED_IMAGE_FORMAT_SEQUENCE
from common import DEFAULT_GENERATE_TYPE, DEFAULT_GENERATE_POSITION


def generate_str_classic(colors, size, top_blank=0, left_blank=0):
    # colors: tuple(tuple(tuple(int, int, int), ...), ...)
    # size: (int, int)
    # top_blank: int
    # left_blank: int

    width, height = size
    if width <= 0 or height <= 0:
        return ""
    if width*height != len(colors)*len(colors[0]):
        raise ValueError('size and colors are not matched')

    return ''.join(
        ['\033[{}B'.format(top_blank) if top_blank > 0 else '',
         '\n'.join(map(lambda line: ''.join(['\033[{}C'.format(left_blank) if left_blank > 0 else '', ''.join(map(lambda color: "\033[48;2;{};{};{}m \033[0m".format(*color), line))]), colors)),
         '\033[{}A'.format(top_blank + height) if top_blank + height > 0 else '',
         '\033[{}D'.format(left_blank + width) if left_blank + width > 0 else '',
         '\033[?25l']
    )


def generate_str_stringio(colors, size, top_blank=0, left_blank=0):
    # colors: tuple(tuple(tuple(int, int, int), ...), ...)
    # size: (int, int)
    # top_blank: int
    # left_blank: int

    try:
        import io
    except ImportError:
        raise ImportError('generate_str_stringio requires io module')

    width, height = size
    if width <= 0 or height <= 0:
        return ""
    if width*height != len(colors)*len(colors[0]):
        raise ValueError('size and colors are not matched')

    out_buffer = io.StringIO()
    if top_blank > 0:
        out_buffer.write('\033[{}B'.format(top_blank))
    for line in colors:
        if left_blank > 0:
            out_buffer.write('\033[{}C'.format(left_blank))
        for color in line:
            out_buffer.write("\033[48;2;{};{};{}m \033[0m".format(*color))
        out_buffer.write('\n')
    # remove the last '\n'
    out_buffer.seek(out_buffer.tell() - 1)
    # back to the original position
    if top_blank + height > 0:
        out_buffer.write('\033[{}A'.format(top_blank + height))
    if left_blank + width > 0:
        out_buffer.write('\033[{}D'.format(left_blank + width))
    # hide the cursor
    out_buffer.write('\033[?25l')

    return out_buffer.getvalue()


def generate_str_numpy(colors, size, top_blank=0, left_blank=0, brightness=0.00):
    # colors: tuple(tuple(tuple(int, int, int), ...), ...)
    # size: (int, int)
    # top_blank: int
    # left_blank: int
    # brightness: float in [-1, 1]

    try:
        import numpy as np
    except ImportError:
        raise ImportError('generate_str_numpy requires numpy module')

    width, height = size
    if width <= 0 or height <= 0:
        return ""
    if width*height != len(colors)*len(colors[0]):
        raise ValueError('size and colors are not matched')

    brightness = min(max(brightness, -0.999), 0.999)

    colors = np.array(colors, dtype=np.int16)
    # hsv: import colorsys
    # hsv: colors = np.array([[colorsys.rgb_to_hsv(*color) for color in line] for line in colors])
    if (brightness < 0.0):
        colors = colors * (1 + brightness)
    elif (brightness > 0.0):
        colors = colors * 1 / (1 - brightness)
    # hsv: colors = np.array([[colorsys.hsv_to_rgb(*color) for color in line] for line in colors])
    colors = (np.clip(colors, 0, 255)).astype(np.uint8)

    return ''.join([
        '\033[{}B'.format(top_blank) if top_blank > 0 else '',

        ''.join((
            np.concatenate((np.char.mod('\033[48;2;%sm \033[0m', np.apply_along_axis(lambda line: np.apply_along_axis(lambda color: ';'.join(map(str, color)), 0, line), 2, colors)), np.full((height, 1), '\n', dtype=np.str_)), axis=1)
            if left_blank <= 0 else
            np.concatenate((np.char.add(np.full((height, 1), '', dtype=np.str_), '\033[{}C'.format(left_blank)), np.concatenate((np.char.mod('\033[48;2;%sm \033[0m', np.apply_along_axis(lambda line: np.apply_along_axis(lambda color: ';'.join(map(str, color)), 0, line), 2, colors)), np.full((height, 1), '\n', dtype=np.str_)), axis=1)), axis=1
        )).flatten()[:-1]),

        '\033[{}A'.format(top_blank + height) if top_blank + height > 0 else '',
        '\033[{}D'.format(left_blank + width) if left_blank + width > 0 else '',
        '\033[?25l'
    ])


def generate_str_multiprocessing(colors, size, top_blank=0, left_blank=0):

    try:
        from concurrent import futures
    except ImportError:
        raise ImportError('generate_str_multiprocessing requires futures module')

    width, height = size
    if width <= 0 or height <= 0:
        return ""
    if width*height != len(colors)*len(colors[0]):
        raise ValueError('size and colors are not matched')

    generate_str_simple = lambda colors, left_blank: '\n'.join(map(lambda line: ''.join(['\033[{}C'.format(left_blank) if left_blank > 0 else '', ''.join(map(lambda color: "\033[48;2;{};{};{}m \033[0m".format(*color), line))]), colors))

    # generate each line of the image, and then concatenate them
    with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        fs = [executor.submit(generate_str_simple, colors[i:i+1], left_blank=left_blank) for i in range(height)]
        return ''.join(
            ['\033[{}B'.format(top_blank) if top_blank > 0 else '',
             '\n'.join([f.result() for f in fs]),
             '\033[{}A'.format(top_blank + height) if top_blank + height > 0 else '',
             '\033[{}D'.format(left_blank + width) if left_blank + width > 0 else '',
             '\033[?25l']
        )


# @lru_cache(maxsize=None)
def generate_str(colors, size, top_blank=0, left_blank=0, generate_type=DEFAULT_GENERATE_TYPE):

    if generate_type == 'classic':
        return generate_str_classic(colors, size, top_blank=top_blank, left_blank=left_blank)
    elif generate_type == 'stringio':
        return generate_str_stringio(colors, size, top_blank=top_blank, left_blank=left_blank)
    elif generate_type == 'numpy':
        return generate_str_numpy(colors, size, top_blank=top_blank, left_blank=left_blank)
    elif generate_type == 'multiprocessing':
        return generate_str_multiprocessing(colors, size, top_blank=top_blank, left_blank=left_blank)
    else:
        raise ValueError('unknown generate_type: {}'.format(generate_type))


def colors2str_one(im_result, *, frame_size=None, pos=None):
    if not isinstance(im_result, Result):
        raise TypeError('im_result must be an instance of Result')
    if im_result.status != Status.done:
        raise ValueError('im_result must be done')

    fmt, width, height, mode, colors = im_result.data
    frame_width, frame_height = frame_size or (width, height)

    if pos is None:
        if DEFAULT_GENERATE_POSITION == 'center':
            pos_x = (frame_width - width) // 2
            pos_y = (frame_height - height) // 2
        elif DEFAULT_GENERATE_POSITION == 'left-top':
            pos_x = 0
            pos_y = 0
        elif DEFAULT_GENERATE_POSITION == 'right-top':
            pos_x = frame_width - width
            pos_y = 0
        elif DEFAULT_GENERATE_POSITION == 'left-bottom':
            pos_x = 0
            pos_y = frame_height - height
        elif DEFAULT_GENERATE_POSITION == 'right-bottom':
            pos_x = frame_width - width
            pos_y = frame_height - height
        else:
            raise ValueError('unknown generate_position: {}'.format(DEFAULT_GENERATE_POSITION))
    else:
        pos_x, pos_y = pos

    if pos_x >= frame_width or pos_y >= frame_height or width <= 0 or height <= 0:
        return ""

    if pos_x < 0:
        colors = colors[:, -pos_x:]
        width += pos_x
        pos_x = 0
    if pos_y < 0:
        colors = colors[-pos_y:, :]
        height += pos_y
        pos_y = 0

    if pos_x + width > frame_width:
        colors = colors[:, :frame_width - pos_x]
        width = frame_width - pos_x
    if pos_y + height > frame_height:
        colors = colors[:frame_height - pos_y, :]
        height = frame_height - pos_y

    if mode == "RGB":
        colors_tuple = tuple(tuple(tuple(color) for color in line) for line in colors)
    elif mode == "RGBA":
        colors_tuple = tuple(tuple(tuple(color[:3]) for color in line) for line in colors)
    elif mode == "1" or mode == "L" or mode == "P":
        colors_tuple = tuple(tuple((color, color, color) for color in line) for line in colors)
    else:
        raise ValueError('unknown mode: {}'.format(mode))

    return generate_str(colors_tuple, (width, height), top_blank=pos_y, left_blank=pos_x)


def colors2str_seq(im_results_seq, *, frame_size=None, pos=None):

    try:
        from concurrent import futures
    except ImportError:
        raise ImportError('colors2str_seq requires futures module')

    if not isinstance(im_results_seq, Result):
        raise TypeError('im_result must be an instance of Result')
    if im_results_seq.status != Status.done:
        raise ValueError('im_result must be done')

    fmt, duration, results = im_results_seq.data

    fs_to = []
    with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for im_result in results:

            _, width, height, mode, colors = im_result.data
            frame_width, frame_height = frame_size or (width, height)

            if pos is None:
                if DEFAULT_GENERATE_POSITION == 'center':
                    pos_x = (frame_width - width) // 2
                    pos_y = (frame_height - height) // 2
                elif DEFAULT_GENERATE_POSITION == 'left-top':
                    pos_x = 0
                    pos_y = 0
                elif DEFAULT_GENERATE_POSITION == 'right-top':
                    pos_x = frame_width - width
                    pos_y = 0
                elif DEFAULT_GENERATE_POSITION == 'left-bottom':
                    pos_x = 0
                    pos_y = frame_height - height
                elif DEFAULT_GENERATE_POSITION == 'right-bottom':
                    pos_x = frame_width - width
                    pos_y = frame_height - height
                else:
                    raise ValueError('unknown generate_position: {}'.format(DEFAULT_GENERATE_POSITION))
            else:
                pos_x, pos_y = pos

            if pos_x >= frame_width or pos_y >= frame_height or width <= 0 or height <= 0:
                fs_to.append(None)
                continue

            if pos_x < 0:
                colors = colors[:, -pos_x:]
                width += pos_x
                pos_x = 0

            if pos_y < 0:
                colors = colors[-pos_y:, :]
                height += pos_y
                pos_y = 0

            if pos_x + width > frame_width:
                colors = colors[:, :frame_width - pos_x]
                width = frame_width - pos_x
            if pos_y + height > frame_height:
                colors = colors[:frame_height - pos_y, :]
                height = frame_height - pos_y

            if mode == "RGB":
                colors_tuple = tuple(tuple(tuple(color) for color in line) for line in colors)
            elif mode == "RGBA":
                colors_tuple = tuple(tuple(tuple(color[:3]) for color in line) for line in colors)
            elif mode == "1" or mode == "L" or mode == "P":
                colors_tuple = tuple(tuple((color, color, color) for color in line) for line in colors)
            else:
                raise ValueError('unknown mode: {}'.format(mode))

            fs_to.append(executor.submit(generate_str, colors_tuple, (width, height), top_blank=pos_y, left_blank=pos_x))

    fs = [ f.result() if f is not None else "" for f in fs_to ]
    fs.append(duration)

    return fs


def colors2str(result, *, frame_size=None, pos=None):
    if not isinstance(result, Result):
        raise TypeError('result must be an instance of Result')
    if result.status != Status.done:
        raise ValueError('result must be done')

    fmt = result.data[0]

    if fmt.lower() in SUPPORTED_IMAGE_FORMAT:
        return colors2str_one(result, frame_size=frame_size, pos=pos)
    elif fmt.lower() in SUPPORTED_IMAGE_FORMAT_SEQUENCE:
        return colors2str_seq(result, frame_size=frame_size, pos=pos)
    else:
        raise ValueError('unknown format: {}'.format(fmt))


if __name__ == '__main__':
    # a little test
    import PIL.Image
    import numpy as np
    orange_img  = PIL.Image.new('RGB', (10, 10), (255, 128, 0))
    blue_img    = PIL.Image.new('RGB', (10, 10), (0, 0, 255))
    red_img     = PIL.Image.new('RGB', (10, 10), (255, 0, 0))
    yellow_img  = PIL.Image.new('RGB', (10, 10), (255, 255, 0))
    orange_result   = Result(Status.done, ('JPEG', 10, 10, orange_img.mode, np.array(orange_img)))
    blue_result     = Result(Status.done, ('JPEG', 10, 10, blue_img.mode, np.array(blue_img)))
    red_result      = Result(Status.done, ('JPEG', 10, 10, red_img.mode, np.array(red_img)))
    yellow_result   = Result(Status.done, ('JPEG', 10, 10, yellow_img.mode, np.array(yellow_img)))
    print(colors2str(orange_result, frame_size=(20, 20), pos=(0, 0)))
    print(colors2str(red_result, frame_size=(20, 20), pos=(0, 10)))
    print(colors2str(blue_result, frame_size=(20, 20), pos=(10, 0)))
    print(colors2str(yellow_result, frame_size=(20, 20), pos=(10, 10)))