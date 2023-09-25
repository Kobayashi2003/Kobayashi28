# 实现删除字符串中出现次数最少的字符，若多个字符中出现的次数一样，则都删除。输出删除这些单词之后的字符串，字符串中其它字符保持原来的顺序

string = input("Please input a string: ")
string_delete = ""

table_set = set(string) # 提取出字符串中所有不重复的字符，并将其存放入table_set中用于之后的检索
cont = [] # 用于存储每个不同字符所出现的次数

for i in table_set:
    cont.append(string.count(i))

min_number = min(cont)

for i in string:
    if string.count(i) != min_number:
        string_delete += i
