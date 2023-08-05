# guess the number

from random import *
count = 0
num = int(random() * 100) + 1
while 1:
    guess_num = input("please input the number you guess: ")
    if not guess_num.isdigit():
        print("wrong input, please try again!")
        continue
    guess_num = int(guess_num)
    count += 1
    if (guess_num == num):
        print("you are right!")
        print(f"you have guessed for {count} times in total")
        if (count > 8):
            print("you have guessed for over 8 times! Please try next time!")
        break
    elif guess_num < num:
        print("too small!")
    else:
        print("too big!")
