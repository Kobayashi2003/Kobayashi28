# 判断一个用户输入的短字符串是否在另一个由用户输入的长字符串中全部出现

short_str = input("Please input a short string: ")
long_str = input("Please input a long string: ")

if short_str in long_str:
    print("True")
else:
    print("False")