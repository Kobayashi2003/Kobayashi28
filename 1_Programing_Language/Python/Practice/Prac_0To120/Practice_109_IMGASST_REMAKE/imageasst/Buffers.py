import win32console
import io
import numpy as np

class Buffers():

    __solts__ = ('num', 'buffer_list', '__current', '__last', '__size', '__origin_buffer')

    def __init__(self, num=2, size=None):
        self.num = num
        if self.num < 2:
            raise ValueError('The number of buffers must be greater than 1.')
        self.__size = win32console.PyCOORDType(*size) if size is not None else None

        self.buffer_list = None
        self.__create__buffers()
        self.__current = 0
        self.__last = 0
        self.__origin_buffer = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for buffer in self.buffer_list:
            buffer.Close()

    def __del__(self):
        self.__origin_buffer.SetConsoleActiveScreenBuffer()
        for buffer in self.buffer_list:
            buffer.Close()

    def __create__buffers(self):
        self.buffer_list = [win32console.CreateConsoleScreenBuffer() for _ in range(self.num)]

    def write(self, output='\n'):
        if isinstance(output, str):
            self.buffer_list[self.__current].WriteConsole(output)
        elif isinstance(output, io.StringIO):
            self.buffer_list[self.__current].WriteConsole(output.getvalue())
        elif isinstance(output, io.TextIOWrapper):
            self.buffer_list[self.__current].WriteConsole(output.read())
        elif isinstance(output, io.BytesIO):
            self.buffer_list[self.__current].WriteConsole(output.getvalue().decode())
        elif isinstance(output, np.ndarray):
            # check the shape and dtype of the array [height*[width*[r, g, b]]]
            if (not output.ndim == 3 or not output.shape[2] == 3):
                raise ValueError('The shape of the array must be 2 and the dtype must be np.uint8.')
            # convert the array to string
            for i in range(output.shape[0]):
                for j in range(output.shape[1]):
                    self.buffer_list[self.__current].WriteConsole('\033[48;2;{};{};{}m \033[0m'.format(*output[i, j]))
                if i < output.shape[0] - 1:
                    self.buffer_list[self.__current].WriteConsole('\n')
        else:
            raise TypeError('The type of output must be str, io.StringIO or io.TextIOWrapper.')

    def switch(self):
        self.__last = self.__current
        self.__current = (self.__current + 1) % self.num
        self.buffer_list[self.__current] = win32console.CreateConsoleScreenBuffer()
        if self.__size is not None:
            self.buffer_list[self.__current].SetConsoleScreenBufferSize(self.__size)

    def flush(self):
        self.buffer_list[self.__current].SetConsoleActiveScreenBuffer()
        self.buffer_list[self.__last].Close()

    def get_current_buffer(self):
        return self.buffer_list[self.__current]

    def set_buffer_size(self, size):
        self.__size = win32console.PyCOORDType(*size)

    def get_buffer_size(self):
        return self.__size

    def scroll(self, DestinationOrigin, ScrollRectangle=None, ClipRectangle=None, Fill=' ', Attribute=0x0f):
        DestinationOrigin = win32console.PyCOORDType(*DestinationOrigin)
        if ScrollRectangle is None:
            ScrollRectangle = win32console.PySMALL_RECTType(0, 0, self.__size.X-1, self.__size.Y-1)
        else:
            ScrollRectangle = win32console.PySMALL_RECTType(*ScrollRectangle)
        if ClipRectangle is None:
            ClipRectangle = win32console.PySMALL_RECTType(0, 0, self.__size.X-1, self.__size.Y-1)
        else:
            ClipRectangle = win32console.PySMALL_RECTType(*ClipRectangle)
        self.buffer_list[self.__current].ScrollConsoleScreenBuffer(ScrollRectangle, ClipRectangle, DestinationOrigin, Fill, Attribute)


if __name__ == '__main__':
    # a little test
    import time
    import shutil
    import random
    import string
    import msvcrt

    terminal_size = shutil.get_terminal_size()
    width, height = terminal_size
    buffers = Buffers(num=2, size=(width*2, height*2))

    def color(str):
        return random.choice(['\033[41m', '\033[42m', '\033[43m', '\033[44m', '\033[45m', '\033[46m']) + str + '\033[0m'

    def generate_str():
        import io
        output = io.StringIO()
        for _ in range(height):
            for _ in range(width):
                output.write(color(random.choice(string.ascii_letters)))
            output.write('\n')
        return output.getvalue()[0:-1] + '\033[?25h'

    # Test1: refresh rate
    def refresh_rate_test():

        # write the string to the buffer
        n = 100
        output_list = [generate_str() for _ in range(n)]

        time_list = []
        switch_time_list = []
        write_time_list = []
        flush_time_list = []

        for output in output_list:
            t_begin = time.perf_counter()

            t_begin_switch = time.perf_counter()
            buffers.switch()
            t_end_switch = time.perf_counter()

            t_begin_write = time.perf_counter()
            buffers.write(output)
            t_end_write = time.perf_counter()

            # During actual operation, printing the text to the
            # terminal will take some time. Sometimes, the program
            # will flush the buffer before the next frame is ready.
            # To avoid this, we can add a little delay here.
            time.sleep(.2)

            t_begin_flush = time.perf_counter()
            buffers.flush()
            t_end_flush = time.perf_counter()

            t_end = time.perf_counter()

            time_list.append(t_end - t_begin)
            switch_time_list.append(t_end_switch - t_begin_switch)
            write_time_list.append(t_end_write - t_begin_write)
            flush_time_list.append(t_end_flush - t_begin_flush)

            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch == b'q':
                    break

        print(sum(time_list)/len(time_list))
        print(sum(switch_time_list)/len(switch_time_list))
        print(sum(write_time_list)/len(write_time_list))
        print(sum(flush_time_list)/len(flush_time_list))

    # Test2: buffer scroll
    def buffer_scroll_test():

        output = generate_str()
        buffers.switch()
        buffers.flush()
        buffers.write(output)

        msvcrt.getch()

        for _ in range(10):
            buffers.scroll((1, 1))
            time.sleep(.05)

        for _ in range(10):
            buffers.scroll((-1, -1))
            time.sleep(.05)

        for _ in range(10): # TODO: the buffer scroll really sucks
            buffers.scroll((-1, -1))
            time.sleep(.05)

        for _ in range(10):
            buffers.scroll((1, 1))
            time.sleep(.05)

    refresh_rate_test()
    buffer_scroll_test()
