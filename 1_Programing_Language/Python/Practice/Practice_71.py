# 求一个 int 类型数字对应的二进制数字中 1 的最大连续数

def the_max_length_of_one(b):
    b_str = str(b)
    str_1 = '1'
    cont = 0
    while str_1 in b_str:
        str_1 += '1'
        cont += 1
    return cont

def the_max_length_of_one_v2(b):
    b_str = str(b)
    MaxLength = 0
    for i in range(len(b_str)):
        if b_str[i] == '1':
            cont += 1
            MaxLength = max(MaxLength, cont)
        else:
            cont = 0
    return MaxLength

b = bin(int(input(), 10))
print(b)
print(the_max_length_of_one(b))
print(the_max_length_of_one_v2(b))