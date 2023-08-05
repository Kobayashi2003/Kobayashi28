l1, l2 = [1, 2, 1, 3, 4, 6, 9], [1, 2, 5, 6, 7]

t1, t2 = tuple(l1), tuple(l2)

s1, s2 = set(l1), set(l2)

# 输出两个列表的交集
intersection = s1 & s2
print(intersection)


# 输出两个列表的交集的遍历
for i in intersection:
    print(i, end=" ")
print("")


# 输出两个列表的并集
union = s1 | s2
print(union)


# 输出并集元素的数目
print(len(union))


# 输出两个列表分别的查缉
difference1 = s1 - s2
difference2 = s2 - s1
print(f"{difference1}\n{difference2}")