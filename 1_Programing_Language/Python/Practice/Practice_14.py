"""
输入一个十进制数并将其以二进制的形式输出
"""

num = int(input("Please input a number:"))

bin = ""
while num > 0:
    bin += str(num%2)
    num //= 2

print(bin[::-1])