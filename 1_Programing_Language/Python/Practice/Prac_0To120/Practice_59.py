# 循环结构应用
# 1. 用户输入一个字符串，实现该字符串的倒序输出
# 2. 用户输入两个参数，第一个参数为一个字符串，第二个参数为一个数字，输出字符串在该数字后全部字符（注意判断数字是否合法）

def reverse_string(str):
    return str[::-1]

def output_string(str, num):
    if num > len(str):
        print('The number is out of range.')
    else:
        return str[num:]

string = input("Please input a string: ")
number = int(input("Please input a number: "))

print(reverse_string(string))
print(output_string(string, number))