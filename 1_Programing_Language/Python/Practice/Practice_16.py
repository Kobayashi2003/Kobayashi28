"""
现在有n个人围成一个圈，每个人的编号分别为1~n，
从1号开始报数，每当一个人报的数是7的倍数的时候，就退出圈圈，其他的人接着继续报数，一直到最后一个人出圈。
比方说现在有七个人围在一起，编号分别为1-7，那么7个人退出队列的顺序分别是：7、1、3、6、2、4、5.
"""

# n = int(input("Please input a number:"))
n = int(input())
people = list(range(1, n+1))

last = 0
while len(people):
    tmp = (last % len(people)+6) % len(people)
    print(people.pop((last % len(people)+6) % len(people)))
    last = tmp
