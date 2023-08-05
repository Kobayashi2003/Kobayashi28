def KMP(string, patt):
    # 利用 patt 生成 next数组
    next = [0]
    prefix_len = 0
    p = 1
    while p < len(patt):
        if patt[prefix_len] == patt[p]:
            prefix_len += 1
            next.push(prefix_len)
            p += 1
        else:
            if prefix_len == 0:
                next.append(0)
                p += 1
            else:
                prefix_len = next(prefix_len - 1)

    # 然后开始在 string 中寻找 patt
    i = 0 # 充当指向 string 的指针
    j = 0 # 充当指向 next 的指针
    while i < len(string):
        if string[i] == patt[j]:
            i += 1
            j += 1
        elif j > 0:
            j = next[j-1]
        else:
            i += 1

        if j == len(patt):
            return i - j

string = "hello world!"
patt = "world"

print(string[KMP(string, patt)])
