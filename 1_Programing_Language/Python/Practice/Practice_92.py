from threading import Thread
import time

def func(*args, **kwargs):
    print(args)
    print(kwargs)

class mthread(Thread):
    def __init__(self, func, *args, **kwargs):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.start_flag = False
        self.end_flag = False

    def run(self):
        self.start_flag = True
        while not self.end_flag:
            self.func(*self.args, **self.kwargs)
            time.sleep(1)
        print('Thread is end')

    def stop(self):
        self.end_flag = True


if __name__ == '__main__':

    th = mthread(func, "hello", "world", a=1, b=2)
    th.start()
    time.sleep(5)
    th.stop() 
        