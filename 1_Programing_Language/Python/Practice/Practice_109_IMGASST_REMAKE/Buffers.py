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
    
    def color(str):
        # return random.choice(['\033[0;31m', '\033[0;32m', '\033[0;33m', '\033[0;34m', '\033[0;35m', '\033[0;36m']) + str + '\033[0m'
        return random.choice(['\033[41m', '\033[42m', '\033[43m', '\033[44m', '\033[45m', '\033[46m']) + str + '\033[0m'
    
    def generate_str():
        import io
        output = io.StringIO()
        for _ in range(terminal_size[0] * terminal_size[1]):
            # output.write(color(random.choice(string.ascii_letters)))
            output.write(color(' '))
        return output.getvalue()

    # write the string to the buffer
    output_list = [generate_str() for _ in range(100)]

    time_list = []

    for output in output_list:
        t_begin = time.perf_counter()
        buffers.switch()
        buffers.write(output)
        buffers.flush()
        input()
        t_end = time.perf_counter()
        time_list.append(t_end - t_begin)
        time.sleep(.1)
    print(time_list)
