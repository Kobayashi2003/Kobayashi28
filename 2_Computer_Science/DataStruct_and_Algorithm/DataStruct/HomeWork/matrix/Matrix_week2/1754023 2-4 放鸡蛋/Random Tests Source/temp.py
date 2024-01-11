import random

n = 5

print(n)

for i in range(n):
        x_start = random.randint(5, 20)
        x_end = random.randint(1, 20)

        print("%d %d" % (x_start,x_end))

