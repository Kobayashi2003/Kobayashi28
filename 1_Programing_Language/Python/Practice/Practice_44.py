# 匿名函数


# - 匿名函数的调用方法：直接赋值给一个变量，然后再像一般函数一样调用

foo1 = lambda x, y : x + y

print(foo1(1,3))

# - 在匿名函数中可以使用 默认值传值

foo2 = lambda x, y=0 : x - y

print(foo2(2))


# - 在匿名函数中可以使用 无名参数

foo3 = lambda *args : args # 将返回一个元组

print(foo3('hello','world'))

# - 在匿名函数中也可以使用 有名参数

foo4 = lambda **kwargs : kwargs # 将返回一个字典

print(foo4())

# - 在匿名函数中可以直接在函数后传递参数


print( (lambda x, y : x if x>y else y)(12, 10) )
