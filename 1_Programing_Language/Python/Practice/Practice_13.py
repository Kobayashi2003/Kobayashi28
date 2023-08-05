"""
定义一个函数，sun_numebrs，可以接收的 任意多个整数
功能要求：将传递的 所有数字累加 并且返回累加结果
"""

def sum_numbers(*args):

    num = 0
    for n in args:
        num += n

    return num

print(sum_numbers(1, 2, 3))


