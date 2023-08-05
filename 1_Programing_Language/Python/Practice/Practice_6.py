# 石头剪刀布

import random

you = int(input("please input your gesture（1. Rock 2. Paper 3. Scissors）:"))

computer = random.randint(1, 3)

if ((you == 1 and computer == 3)
        or (you == 2 and computer == 1)
        or (you == 3 and computer == 2)):
    print("you win!")
elif you == computer :
    print("tie")
else :
    print("you lose!")