# generater_list = (i*i for i in range(0, 10))
# print(generater_list)

# 尝试模仿 生成器的语法糖

# list = [i*i for i in range(0, 10)]
# print(list)


def generator_list(x, y):
    for i in range(x, y):
        yield i


def create_list(x, y):
    g = generator_list(x, y)
    list = []
    # for i in range(x, y):
    for i in g:
        # i = next(g)
        list.append(i*i)
    return list


l = create_list(0, 10)
print(l)