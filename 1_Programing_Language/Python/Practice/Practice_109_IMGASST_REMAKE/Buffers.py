import win32console

class Buffers():
    def __init__(self, num=2):
        self.num = num
        self.buffer_list = None
        self.__create__buffers()
        self.__current = 0
        self.__last = 0

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        for buffer in self.buffer_list:
            buffer.Close()

    def __del__(self):
        for buffer in self.buffer_list:
            buffer.Close()

    def __create__buffers(self):
        self.buffer_list = [win32console.CreateConsoleScreenBuffer() for _ in range(self.num)]

    def write(self, str='\n'):
       self.buffer_list[self.__current].WriteConsole(str)

    def switch(self):
        self.__last = self.__current
        self.__current = (self.__current + 1) % self.num
        self.buffer_list[self.__current] = win32console.CreateConsoleScreenBuffer()

    def flush(self):
        self.buffer_list[self.__current].SetConsoleActiveScreenBuffer()
        self.buffer_list[self.__last].Close()



if __name__ == '__main__':
    import time
    import shutil
    terminal_size = shutil.get_terminal_size()
    buffers = Buffers(num=5)
    import random
    import string
    import msvcrt
    
    def color(str):
        return random.choice(['\033[0;31m', '\033[0;32m', '\033[0;33m', '\033[0;34m', '\033[0;35m', '\033[0;36m']) + str + '\033[0m'
        # return random.choice(['\033[41m', '\033[42m', '\033[43m', '\033[44m', '\033[45m', '\033[46m']) + str + '\033[0m'
    
    def generate_str():
        import io
        output = io.StringIO()
        for _ in range(terminal_size[0] * terminal_size[1]):
            output.write(color(random.choice(string.ascii_letters)))
            # output.write(color(' '))
        return output.getvalue()

    # write the string to the buffer
    n = 100
    output_list = [generate_str() for _ in range(n)]

    time_list = []

    # Test1: frame to frame
    for output in output_list:
        t_begin = time.perf_counter()
        buffers.switch()
        buffers.write(output)
        buffers.flush()
        t_end = time.perf_counter()
        time_list.append(t_end - t_begin)

        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == b'q':
                break

        # time.sleep(.1)


    # Test2: scroll
    # buffers.switch()
    # buffers.write(output_list[0])
    # buffers.flush()

    # msvcrt.getch()

    # buf = buffers.buffer_list[1]
    # width, height = shutil.get_terminal_size()

    # # move directly
    # t_begin = time.perf_counter()
    # buf.ScrollConsoleScreenBuffer(win32console.PySMALL_RECTType(0, 0, width-1, height//2), None, win32console.PyCOORDType(0, height//2), '#', 0x0f)
    # t_end = time.perf_counter()
    # time_list.append(t_end - t_begin)

    # msvcrt.getch()

    # # move line by line
    # for i in range(0, height // 2):
    #     t_begin = time.perf_counter()
    #     buf.ScrollConsoleScreenBuffer(win32console.PySMALL_RECTType(0, i, width-1, height-1), None, win32console.PyCOORDType(0, i+1), '#', 0x0f)
    #     t_end = time.perf_counter()
    #     time_list.append(t_end - t_begin)
    
    # msvcrt.getch()

    print(time_list)
