# 24点判断：给出 4 个数字，使用加减乘除和括号，计算出 24

# 递归解法

import random
from copy import deepcopy


def cal24(a, b, c, d):

    cont = 0
    memo = []
    answers = []

    def handing_two_nums(x, y):
        result = []
        result.append(x + y)
        result.append(x * y)
        result.append(x - y)
        result.append(y - x)
        if x != 0:
            result.append(y / x)
        if y != 0:
            result.append(x / y)

        return result

    def find_answers(*args):
        # 递归的主要思路就是四个变三个算，三个变两个算，然后枚举出全部的可能性
        nonlocal cont, memo, answers

        nums = len(args)
        # 枚举所有数两两组合的情况
        for i in range(nums - 1):
            for j in range(i + 1, nums):
                # print(f"{args[i]} {args[j]}")
                last_nums = list(args)
                last_nums.remove(args[i])
                last_nums.remove(args[j])

                # 现在要做的就是先将 args 中的其中两个数枚举所有的四则运算并每种情况得出一个新数，并将这三个数扔到递归中
                result = (handing_two_nums(args[i], args[j]))

                for index, k in enumerate(result):
                    memo.append("+*--//"[index])
                    if last_nums == []:
                        if k == 24:
                            cont += 1
                            answers.append(deepcopy(memo))
                    else:
                        find_answers(*last_nums, k)
                    memo.pop()


    find_answers(a, b, c, d)
    judge = True if cont > 0 else False
    # if judge:
    #     print(answers[0])
    return judge


def generate_numbers():

    while True:
        numbers = [random.randint(0, 20) for i in range(4)]
        if cal24(*numbers):
            print(numbers)
            break
