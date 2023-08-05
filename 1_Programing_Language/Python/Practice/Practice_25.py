# 在计算机随机生成的 N 个 1~100 之间的随机整数（N<=100），N 由用户输入，对于其中重复的数字只保留一个，然后把这些数从小到大进行排序并输出

from random import randint

N = int(input("Please input a number: "))
num_list = [randint(1, 101) for i in range(0, N)]

# 去重
num_set = set(num_list)

# 排序
num_list_new = list(num_list)
num_list_new.sort()
