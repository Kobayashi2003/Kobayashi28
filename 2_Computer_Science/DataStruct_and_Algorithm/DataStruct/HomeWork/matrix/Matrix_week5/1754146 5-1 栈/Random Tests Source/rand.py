
import random

T = random.randint(50, 100)
for i in range(T):
    n = random.randint(100, 100000)
    print(n)
    for _ in range(n):
        k = random.randint(0, 3)
        if k <= 2:
            x = random.randint(0, 99999999)
            print(f"0 {x}")
        else:
            op = random.randint(1, 3)
            print(op)
    print()