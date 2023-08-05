# 构造一个不少于 20 个数值的列表，从小到大排序后，选取前 5 个元素并计算其平方值
from random import randint
nums = [randint(0, 100000) for i in range(0, 20)]

nums.sort()

for i in range(0, 5):
    print(f"{nums[i]**2} ")