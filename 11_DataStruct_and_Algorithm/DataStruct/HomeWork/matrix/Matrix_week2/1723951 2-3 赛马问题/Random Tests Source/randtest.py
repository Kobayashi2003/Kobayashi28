import random


k = random.randint(5,20)

print(k)
for i in range(k):
    if i != k-1:
        val = random.randint(12,200)
        print(str(val)+' ',end='')
    else:
        val = random.randint(12,200)
        print(str(val))

for i in range(k):
    if i != k-1:
        val = random.randint(12,200)
        print(str(val)+' ',end='')
    else:
        val = random.randint(12,200)
        print(str(val))