
def count_times(string : str) -> int:
    chs1 = "adgjmptw"
    chs2 = "behknqux"
    chs3 = "cfilorvy"
    chs4 = "sz"

    times = 0

    for ch in string:
        if ch in chs1:
            times += 1
        elif ch in chs2:
            times += 2
        elif ch in chs3:
            times += 3
        elif ch in chs4:
            times += 4
        elif ch == " ":
            times += 1

    return times

if __name__ == "__main__":
    str = input()
    print(count_times(str))