# 递归函数实现斐波那契数列，以列表形式打印前一百个值

fib = [1, 1]

def fibo(n):
    if n == 1 or n == 2:
        return 1
    else:
        num = fibo(n-1) + fibo(n-2)
        if num not in fib:
            fib.append(num)
        return num

fibo(10)
print(fib)