# 函数累加器

def add():
    cont = 0
    def demo():
        nonlocal cont
        cont += 1
        print(cont)
    return demo

foo = add()

for i in range(0, 10):
    foo()