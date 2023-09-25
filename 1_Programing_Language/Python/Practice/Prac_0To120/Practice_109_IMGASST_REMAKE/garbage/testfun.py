from time import sleep

def test1(*args, **kwargs):
    sleep(3)
    print("test1")
    return args, kwargs
    
def test2():
    sleep(1)
    print("test2")
    return 2