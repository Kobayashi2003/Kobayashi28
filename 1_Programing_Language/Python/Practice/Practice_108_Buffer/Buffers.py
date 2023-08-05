import win32console

class Buffers():
    def __init__(self, num=2):
        '''
        create multi buffers for console
        '''
        self.num = num
        self.buffer_list = []
        self.__create__buffers()
        self.__current = 0
        self.__last = 0

    def __create__buffers(self):
        for _ in range(self.num):
            self.buffer_list.append(win32console.CreateConsoleScreenBuffer())        

    def print(self, str='\n'):
        '''
        output content to buffer
        '''
        self.buffer_list[self.__current].WriteConsole(str)

    def switch(self):
        '''
        switch to next buffer
        '''
        self.__last = self.__current
        self.__current = (self.__current + 1) % self.num
        self.buffer_list[self.__current] = win32console.CreateConsoleScreenBuffer()

    def flash(self):
        '''
        show the buffer
        '''
        self.buffer_list[self.__current].SetConsoleActiveScreenBuffer()
        self.buffer_list[self.__last].Close()
