# 高阶函数的应用

def Sort(x, y, regulation):

    try:
        if regulation(x, y):
            x += y
            y = x - y
            x = x - y
    except Exception as result:
        print(result)

    return x, y


def Cmp1(x, y):
    return x < y


def Cmp2(x, y):
    return x > y


x = 1
y = 2
x, y = Sort(x, y, Cmp1)
print(f"x:{x}, y:{y}")
x, y = Sort(x, y, Cmp2)
print(f"x:{x}, y:{y}")
