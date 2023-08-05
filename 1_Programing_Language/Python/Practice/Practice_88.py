def show_color(str, r, g, b) :
    try:
        r = int(r)
        g = int(g)
        b = int(b)
    except:
        print("The RGB value should be integer.")
        exit()
    print("\033[48;2;{};{};{}m{}\033[0m".format(r, g, b, str), end = "")



if __name__ == "__main__":
    for r in range(256):
        show_color(" ", r, 0, 0)
        if (r + 1) % 64 == 0:
            print()
    print()
    for g in range(256):
        show_color(" ", 0, g, 0)
        if (g + 1) % 64 == 0:
            print()
    print()
    for b in range(256):
        show_color(" ", 0, 0, b)
        if (b + 1) % 64 == 0:
            print()
    print()