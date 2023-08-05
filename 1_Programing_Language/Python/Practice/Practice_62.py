# 写一个函数 prime_factors，使得其输入一个正整数，按照从小到大的顺序输出它的所有质数的因子，（如180的质数因子为 2 2 3 3 5）
# 最后一个数后面也要以换行符结尾

def prime_factors(num):
    factors = []
    divisor = 2
    while num > 1:
        while num % divisor == 0:
            factors.append(divisor)
            num /= divisor
        divisor += 1
    return factors
