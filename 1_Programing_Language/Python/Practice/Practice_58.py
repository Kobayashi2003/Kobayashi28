def fib(max):
    n, before, after = 0, 0, 1
    while n < max:
        yield after
        before, after = after, before + after
        n += 1
    return 'done'


g = fib(10)
while True:
    try:
        x = next(g)
        print('g:', x)
    except StopIteration as e:
        print('Generator return value:', e.value)
        break