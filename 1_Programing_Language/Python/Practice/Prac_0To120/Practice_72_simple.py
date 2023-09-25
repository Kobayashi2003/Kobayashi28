# 判断四个数是否能够计算出24点

def Cal24(a, b, c, d):

    flg = False

    def cal24(*args):
        nonlocal flg
        if flg:
            return

        l = len(args)
        for i in range(l-1):
            for j in range(i+1, l):
                last_nums = list(args)
                last_nums.remove(args[i])
                last_nums.remove(args[j])

                results = []
                results.append(args[i] + args[j])
                results.append(args[i] * args[j])
                results.append(args[i] - args[j])
                results.append(args[j] - args[i])
                if args[j] != 0:
                    results.append(args[i] / args[j])
                if args[i] != 0:
                    results.append(args[j] / args[i])

                for result in results:
                    if last_nums == []: # 算完4个数判断结果
                        if result == 24:
                            flg = True
                    else:
                        cal24(*last_nums, result) # 没算完继续算
    cal24(a, b, c, d)
    return flg

print(Cal24(2, 3, 3, 4))