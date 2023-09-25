def Test():

    num = 1

    def a():
        return num + 1

    def b():
        return num - 1

    return a, b

test1, test2 = Test()


def Test2():

    num = 1

    def a():
        nonlocal num
        num += 1
        return num

    def b():
        nonlocal num
        num -= 1
        return num

    return a, b


test3, test4 = Test2()
test5, test6 = Test2()