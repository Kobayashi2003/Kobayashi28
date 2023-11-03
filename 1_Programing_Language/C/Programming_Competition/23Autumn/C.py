def Solution():

    n, m = map(int, input().split())

    Map1 = []

    for i in range(m):
        a, b = map(int, input().split())
        if (len(Map1) == 0):
            Map1.append(set([a, b]))
        else:
            flag = False
            for j in range(len(Map1)):
                if (a in Map1[j] or b in Map1[j]):
                    Map1[j].add(a)
                    Map1[j].add(b)
                    flag = True
                    break
            if (flag == False):
                Map1.append(set([a, b]))

    k = int(input())

    Map2 = []
    for i in range(k):
        a, b = map(int, input().split())
        if (len(Map2) == 0):
            Map2.append(set([a, b]))
        else:
            flag = False
            for j in range(len(Map2)):
                if (a in Map2[j] or b in Map2[j]):
                    Map2[j].add(a)
                    Map2[j].add(b)
                    flag = True
                    break
            if (flag == False):
                Map2.append(set([a, b]))

    for i in range(n):
        if (i+1 not in Map1):
            Map1.append(set([i+1]))
        if (i+1 not in Map2):
            Map2.append(set([i+1]))

    res = []
    for i in range(len(Map1)):
        for j in range(len(Map2)):
            if (len(Map1[i] & Map2[j]) != 0):
                res.append(Map1[i] & Map2[j])

    min = n + 1
    max = 1

    for i in range(len(res)):
        if (len(res[i]) > max):
            max = len(res[i])
        if (len(res[i]) < min):
            min = len(res[i])

    print(f"{max} {min}")



if __name__ == '__main__':
    Solution()