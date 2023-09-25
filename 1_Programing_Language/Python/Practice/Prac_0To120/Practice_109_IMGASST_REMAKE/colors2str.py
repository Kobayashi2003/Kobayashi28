from io import StringIO
from functools import lru_cache
from concurrent import futures

from common import Result, Status, MAX_WORKERS, SUPPORTED_IMAGE_FORMAT, SUPPORTED_IMAGE_FORMAT_SEQUENCE


@lru_cache(maxsize=None)
def generate_str(colors, size, top_blank=0, left_blank=0):
    width, height = size
    c_width, c_height = len(colors[0]), len(colors)
    if width*height != len(colors)*len(colors[0]):
        raise ValueError('size and colors are not matched')
    out_buffer = StringIO()
    if top_blank > 0:
        out_buffer.write('\033[{}B'.format(top_blank))
    for i, line in enumerate(colors):
        if left_blank > 0:
            out_buffer.write('\033[{}C'.format(left_blank))
        for color in line:
            out_buffer.write("\033[48;2;{};{};{}m \033[0m".format(*color))
        if i + 1 < height:
            out_buffer.write('\n')
    out_buffer.write('\033[?25l')
    return out_buffer.getvalue()


def data_preprocess_one(im_result, *, frame_size=None, pos=(0, 0)):
    if not isinstance(im_result, Result):
        raise TypeError('im_result must be an instance of Result')
    if im_result.status != Status.done:
        raise ValueError('im_result must be done')

    fmt, width, height, mode, colors = im_result.data
    frame_width, frame_height = frame_size or (width, height)
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


def data_preprocess_seq(im_results_seq, *, frame_size=None, pos=(0, 0)):
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


def data_preprocess(result, *, frame_size=None, pos=(0, 0)):
    if not isinstance(result, Result):
        # raise TypeError('result must be an instance of Result')
        return "Some error occurred"
    if result.status != Status.done:
        # raise ValueError('result must be done')
        return result.data 

    fmt = result.data[0]

    if fmt.lower() in SUPPORTED_IMAGE_FORMAT:
        return data_preprocess_one(result, frame_size=frame_size, pos=pos)
    elif fmt.lower() in SUPPORTED_IMAGE_FORMAT_SEQUENCE:
        return data_preprocess_seq(result, frame_size=frame_size, pos=pos)
    else:
        raise ValueError('unknown format: {}'.format(fmt))
