#  用普通函数实现斐波那契数列，并打印前 100 个值，以列表的格式输出

def fibo(n):
    fib = [1, 1]
    if n == 1:
        return [1]
    elif n == 2:
        return fib
    else:
        while n-2:
            fib.append(fib[-1] + fib[-2])
            n -= 1
    return fib

print(fibo(1))