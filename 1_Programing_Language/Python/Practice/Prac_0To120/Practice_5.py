# 老题：输出质数

number = int(input("please input a number:"))

i = 2
while i <= number:
    j = 2
    while j <= i**(1/2):
        if i % j == 0:
            break
        j += 1
    if j > i**(1/2):
        print(f"{i} ")
    i += 1