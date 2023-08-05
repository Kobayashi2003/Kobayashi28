# n 以内的自守数判断

def is_self_num(n):
    if n < 10:
        return True
    str_n = str(n)
    str_n2 = str(n * n)
    if str_n2.endswith(str_n):
        return True
    return False


n = int(input("Please input a number: "))
for i in range(n + 1):
    if is_self_num(i):
        print(i)

    