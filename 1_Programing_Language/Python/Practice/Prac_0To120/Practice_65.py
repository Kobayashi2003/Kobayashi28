def build_next(patt):
    """计算 next 数组"""

    next = [0] # next 数组 （初值元素一个 0）
    prefix_len = 0 # 当前共同前后缀的长度
    i = 1
    while i < len(patt):
        if patt[prefix_len] == patt[i]:
            prefix_len += 1
            next.append(prefix_len)
            i += 1
        else:
            if prefix_len == 0:
                next.append(0)
                i += 1
            else:
                prefix_len = next[prefix_len - 1]
    return next


def kmp_search(string, patt):
    next = build_next(patt)

    i = 0 # 主串中的指针
    j = 0 # 字串中的指针
    while i < len(string):
        if string[i] == patt[j]: # 字符匹配，指针后移
            i += 1
            j += 1
        elif j > 0: # 字符失配，根据 next 跳过子串前面的一些字符
            j = next[j - 1]
        else:
            i += 1

        if j == len(patt): # 匹配成功
            return i - j


msg = 'ABSBABSBABSBXBABXBCNSBFAABACABAfdshajhfhdsajfhdsjkl'
print(kmp_search(msg, 'ABACABA'))