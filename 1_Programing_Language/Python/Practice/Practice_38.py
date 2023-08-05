# 输出 7 有关的数字的个数，其中包括 7 的倍数，还有包含 7 的数字的个数

cont = 0
nums = []
for i in range(0, 10000):
    if i % 7 == 0 or '7' in str(i):
        cont += 1
        nums.append(i)
