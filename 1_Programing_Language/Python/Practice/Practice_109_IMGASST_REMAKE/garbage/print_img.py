import io
import sys
import time

import Buffers
from common import Result, Status, MAX_WORKERS, clock

def print_img(im_result, *, buffer=Buffers.Buffers(), frame_size=None, pos=(0, 0)):
    """print the image"""
    if not isinstance(im_result, Result):
        raise TypeError('im_result must be an instance of Result')
    if im_result.status != Status.done:
        raise ValueError('im_result must be done')

    # colors is a numpy array
    fmt, width, height, mode, colors = im_result.data
    frame_width, frame_height = frame_size or (width, height)
    out_buffer = io.StringIO()

    pos_x, pos_y = pos
    if pos_x < 0:
        colors = colors[:, -pos_x:]
    if pos_y < 0:
        colors = colors[-pos_y:, :]
    if pos_y > 0:
        out_buffer.write('\033[{}B'.format(pos_y))

    if pos_x > frame_width or pos_y > frame_height:
        buffer.switch()
        buffer.write('\033[?25l')
        buffer.flush()
        return

    for i, line in enumerate(colors):
        if not i + pos_y < frame_height:
            break
        if pos_x > 0:
            out_buffer.write('\033[{}C'.format(pos_x))
        for j, color in enumerate(line):
            if not j + pos_x < frame_width:
                break
            if mode == 'RGB':
                out_buffer.write("\033[48;2;{};{};{}m \033[0m".format(*color))
            elif mode == '1' or mode == 'L' or mode == 'P':
                out_buffer.write("\033[48;2;{};{};{}m \033[0m".format(color, color, color))
            elif mode == 'RGBA':
                out_buffer.write("\033[48;2;{};{};{}m \033[0m".format(*color[:3]))
            else:
                raise ValueError('unknown mode: {}'.format(mode))
        if i + pos_y + 1 < frame_height:
            out_buffer.write('\n')
    out_buffer.write('\033[?25l')

    content = out_buffer.getvalue()
    buffer.switch()
    buffer.write(content)
    buffer.flush()


def print_img_sequence(im_results, *, buffer=Buffers.Buffers(), frame_size=None, pos=(0, 0)):
    """print the image sequence"""
    if not isinstance(im_results, Result):
        raise TypeError('im_result must be an instance of Result')
    if im_results.status != Status.done:
        raise ValueError('im_result must be done')

    fmt, duration, results = im_results.data

    first_frame = results[0]
    _, width, height, mode, _ = first_frame.data

    frame_width, frame_height = frame_size or (width, height)
    if pos[0] > frame_width or pos[1] > frame_height:
        buffer.switch()
        buffer.write('\033[?25l')
        buffer.flush()
        return

    fs_colors = [result.data[-1] for result in results]

    def process1frame(frame_colors):
        nonlocal frame_width, frame_height, mode, pos
        out_buffer = io.StringIO()
        pos_x, pos_y = pos
        if pos_x < 0:
            frame_colors = frame_colors[:, -pos_x:]
        if pos_y < 0:
            frame_colors = frame_colors[-pos_y:, :]
        if pos_y > 0:
            out_buffer.write('\033[{}B'.format(pos_y))

        for i, line in enumerate(frame_colors):
            if not i + pos_y < frame_height:
                break
            if pos_x > 0:
                out_buffer.write('\033[{}C'.format(pos_x))
            for j, color in enumerate(line):
                if not j + pos_x < frame_width:
                    break
                if mode == 'RGB':
                    out_buffer.write("\033[48;2;{};{};{}m \033[0m".format(*color))
                elif mode == '1' or mode == 'L' or mode == 'P':
                    out_buffer.write("\033[48;2;{};{};{}m \033[0m".format(color, color, color))
                elif mode == 'RGBA':
                    out_buffer.write("\033[48;2;{};{};{}m \033[0m".format(*color[:3]))
                else:
                    raise ValueError('unknown mode: {}'.format(mode))
            if i + pos_y + 1 < frame_height:
                out_buffer.write('\n')
        out_buffer.write('\033[?25l')
        return out_buffer.getvalue()

    from concurrent import futures
    with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        fs_todo = [executor.submit(process1frame, frame_colors) for frame_colors in fs_colors]
        fs = [f.result() for f in fs_todo]

    from itertools import cycle
    for f in (fs):
        buffer.switch()
        buffer.write(f)
        buffer.flush()
        time.sleep(duration / 1000)
    