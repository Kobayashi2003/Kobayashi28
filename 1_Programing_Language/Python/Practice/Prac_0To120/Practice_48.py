"""
A function next_int(min, max) – this should call the next method to get a random number, then
use addition, subtraction, and the modulus operator % to adjust the random number to be in
between the minimum and maximum number (inclusive). This can, in general, be done with an
equation like so: N%RANGE + min where range indicates how many possible numbers we want to
generate. Make sure you test this function by asking it generate a lot of numbers – mistakes
in a function like this can be hard to ﬁnd, and cause hard to diagnose issues in your code.
"""

# 写一个函数，接收一个范围，生成一个范围内的随机数


# 假设我现在已经存在了一个在超大范围内的随机数

from random import randint

a_random_num = randint(0, 100000000)

def next_int(min=0, max=100):
    # return (max-min) % a_random_num + min 只能说两个写法原理都差不多，但实际用还得看具体情况来选
    return a_random_num % (max-min) + min

f = next_int