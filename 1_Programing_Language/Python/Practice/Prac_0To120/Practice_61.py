# 用户输入两个字符串，一长一短，判断用户输入的短字符串中的所有字符是否在另一个由用户输入的长字符串中全部出现、


def appear(short, long):
    for i in short:
        if i not in long:
            return False
    return True


string1, string2 = input("Please input the first string: "), input("Please input the second string: ")

# 注意保证当两输入的字符串长度相等的时候能够将两个字符串分别赋给short跟long
short_str = string1 if len(string1) < len(string2) else string2
long_str = string2 if len(string2) > len(string1) else string1

print(appear(short_str, long_str))
