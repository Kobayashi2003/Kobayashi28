import time
from threading import Thread

def foo(number):
    time.sleep(number)
    print(number)
    return number

class MyThread(Thread):

    def __init__(self, number):
        Thread.__init__(self)
        self.number = number

    def run(self):
        self.result = foo(self.number)

    def get_result(self):
        return self.result

if __name__ == "__main__":

    thds = []
    for i in range(5):
        thd = MyThread(i)
        thd.start()
        thds.append(thd)
    
    print("test")

    for thd in thds:
        thd.join()
        print(thd.get_result())

    thd1 = MyThread(5)
    thd2 = MyThread(3)
    thd3 = MyThread(4)

    thd1.start()
    thd2.start()
    thd3.start()

    print("test")

    thd1.join()
    thd2.join()
    thd3.join()

    print(thd1.get_result())
    print(thd2.get_result())
    print(thd3.get_result())
