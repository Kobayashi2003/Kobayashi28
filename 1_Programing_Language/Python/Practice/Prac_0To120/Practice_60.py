# 函数 print_string, 连续输入长度不小于 16 的字符串，请按长度为 8 拆分每个字符串，并输出到新的字符串数组。
# 长度不是 8 整数倍的字符串请在后面补数字 0，空字符串不处理。


def print_string():
    list = []
    while True:
        string = input('Please input a string: ')
        if len(string) < 16:
            print('The length of the string is less than 16.')
            continue
        else:
            for i in range(0, len(string), 8):
                list.append(string[i:i+8])
            break
    return list

l = print_string()

for str in l:
    while len(str) < 8:
        str += '0'
    print(str)
