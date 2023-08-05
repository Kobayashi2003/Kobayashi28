# 本联系主要用于演示 yeild关键字 以及 next()函数、send() 方法的用法

def foo():
    print("startint...")
    while True:
        res = yield 4
        print("res:", res)

g = foo()
print(next(g))
print("*" * 50)
print(next(g))
print("*" * 50)
print(g.send(7))