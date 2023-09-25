import Buffers
import time
import os

# get terminal size
width, height = 0, 0
try:
    width, height = os.get_terminal_size().columns, os.get_terminal_size().lines
except:
    print('Error: can not get terminal size')
    exit()

buffer = Buffers.Buffers(5)
n = 0

while (n < height * width):
    buffer.switch()
    # 实心方块
    output = "▇" * width * height
    output = output[:n % (width * height)] + "\033[31m▇\033[0m"+ output[n % (width * height) + 1:]
    buffer.print(output)
    buffer.flash()
    time.sleep(0.01)
    n += 1