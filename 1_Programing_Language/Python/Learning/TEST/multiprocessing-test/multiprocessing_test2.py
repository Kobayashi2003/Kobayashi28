from multiprocessing import Process
from time import sleep

def func1():
    for i in range(10):
        sleep(0.5)
        print('func1: {}'.format(i))

def func2():
    for i in range(5):
        sleep(1)
        print('func2: {}'.format(i))

def main():
    print(sleep)
    p1 = Process(target=sleep, args=(10, ))
    p2 = Process(target=sleep, args=(5,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    main()