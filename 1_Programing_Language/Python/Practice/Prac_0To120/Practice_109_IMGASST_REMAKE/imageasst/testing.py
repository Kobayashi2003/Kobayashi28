def testing():
    import os
    import json
    import msvcrt

    from PIL import Image

    from Buffers import Buffers
    from colors2str import colors2str
    from color_extraction import color_extraction

    from common import get_terminal_size, calculate_aspect_ratio
    from common import ADVANCED_MODE_CODE, SIMPLE_MODE_CODE, TEST_MODE_CODE

    try:
        aspect_ratio_table = json.load(open(os.path.join(os.path.dirname(__file__), 'aspect_ratio_table.json'), 'r'))
    except:
        aspect_ratio_table = {}
    if len(aspect_ratio_table) != 0:
        aspect_ratio_table = { float(key): value for key, value in aspect_ratio_table.items() }

    buffers = Buffers(num=2)
    restart_flg = False
    change_simple_mode_flg = False
    change_advanced_mode_flg = False

    white_square = Image.new('RGB', (1, 1), (255, 255, 255))
    white_square.format = 'PNG'
    edge_len = 1
    aspect_ratio = 1.0
    lst_t_size = (1, 1)
    update_flg = False

    while 1:

        terminal_size = get_terminal_size()
        if lst_t_size != terminal_size:
            lst_t_size = terminal_size
            update_flg = True

        if update_flg:
            edge_len = min(terminal_size) * 2 // 3
            white_square.close()
            white_square = Image.new('RGB', (edge_len, edge_len), (255, 255, 255))
            white_square.format = 'PNG'
            os.system('cls')
            print(colors2str(color_extraction(white_square, mode='RGB', aspect_ratio=aspect_ratio), frame_size=terminal_size, pos=((terminal_size[0] - edge_len) // 2, (terminal_size[1] - edge_len) // 2)))
            print("aspect_ratio:  %0.2f" % aspect_ratio)
            print("terminal_size: %d x %d" % terminal_size)
            print("image_size:    %d x %d" % (edge_len, edge_len))
            update_flg = False

        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'q' or key == b'\x1b':
                break
            elif key == b'j':
                aspect_ratio = max(0.01, aspect_ratio - 0.01)
                update_flg = True
            elif key == b'k':
                aspect_ratio = min(3.0, aspect_ratio + 0.01)
                update_flg = True
            elif key == b'J':
                aspect_ratio = max(0.01, aspect_ratio - 0.1)
                update_flg = True
            elif key == b'K':
                aspect_ratio = min(3.0, aspect_ratio + 0.1)
                update_flg = True
            elif key == b' ' or key == b'\x0d':
                aspect_ratio_table[terminal_size[0] / terminal_size[1]] = aspect_ratio
            elif key == b'c':
                aspect_ratio = calculate_aspect_ratio(terminal_size, aspect_ratio_table)
                update_flg = True

            elif key == b'R':
                restart_flg = True
                break
            elif key == b'A':
                change_advanced_mode_flg = True
                break
            elif key == b'S':
                change_simple_mode_flg = True
                break

    os.system('cls')

    aspect_ratio_table = dict(sorted(aspect_ratio_table.items(), key=lambda item: item[0]))
    with open(os.path.join(os.path.dirname(__file__), 'aspect_ratio_table.json'), 'w') as f:
        json.dump(aspect_ratio_table, f, indent=4)

    if restart_flg:
        return TEST_MODE_CODE
    if change_advanced_mode_flg:
        return ADVANCED_MODE_CODE
    if change_simple_mode_flg:
        return SIMPLE_MODE_CODE
    return 0

if __name__ == '__main__':
    testing()
