# show video cover

import os
import chafa
import ffmpeg
import PIL.Image
import argparse


def show_video_cover(input_file, size):
    """show video cover"""

    video = ffmpeg.input(input_file)
    cover = ffmpeg.output(video, 'pipe:', vframes=1, format='image2', loglevel='error')
    process = ffmpeg.run_async(cover, pipe_stdout=True)
    image = PIL.Image.open(process.stdout)

    width  = image.width
    height = image.height
    bands  = len(image.getbands())
    pixels = image.tobytes()

    config = chafa.CanvasConfig()

    config.width, config.height = size

    term_db   = chafa.TermDb()
    term_info = term_db.detect()
    capabilities = term_info.detect_capabilities()
    config.canvas_mode = capabilities.canvas_mode
    config.pixel_mode  = capabilities.pixel_mode

    FONT_WIDTH  = 11
    FONT_HEIGTH = 24
    config.calc_canvas_geometry(width, height, FONT_WIDTH / FONT_HEIGTH)

    symbol_map = chafa.SymbolMap()
    symbol_map.add_by_tags(chafa.SymbolTags.CHAFA_SYMBOL_TAG_ASCII)
    config.set_symbol_map(symbol_map)

    canvas = chafa.Canvas(config)
    canvas.draw_all_pixels(
        chafa.PixelType.CHAFA_PIXEL_RGB8,
        pixels,
        width,
        height,
        width * bands
    )
    return canvas.print().decode()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Input video file')
    parser.add_argument('-s', '--size', type=str, required=True, help='Terminal size')
    args = parser.parse_args()
    input_file = args.input
    size = (args.size.split('x')) if args.size else None

    size = (int(size[0]), int(size[1]))
    result = show_video_cover(input_file, size)

    import sys
    sys.stdout.write(result)