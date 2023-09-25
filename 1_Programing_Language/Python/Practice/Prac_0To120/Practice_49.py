# 此程序用于尝试模拟 语法糖修饰器的实现

import time


def package(foo):
    def runTime():
        start_time = time.time()
        foo()
        end_time = time.time()
        spent_time = end_time - start_time
        print(f"spent time is: {spent_time}")
    return runTime

@package
def foo():
    time.sleep(1)
    print("Hello world!")
    time.sleep(1)


# foo = package(foo)
# foo()
