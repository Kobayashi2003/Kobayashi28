"""
有两个整数变量 a = 6, b = 100
不使用其它变量，交换两个变量的值
"""


"""
解法1：
num1 = 6
num2 = 100

num1 += num2
num2 = num1 - num2
num1 = num2 - num1
"""

# Python特性，利用元组
a = 6
b = 100
a, b = b, a # 等号右边是一个元组，只是将小括号省略
print(a, b)