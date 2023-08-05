import threading
import functools


def parallel_run(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


@parallel_run
def test():
    import time
    for i in range(10):
        print(f'test {i}')
        time.sleep(1)


def main():
    test()
    print('main')


if __name__ == '__main__':
    main()