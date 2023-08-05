def color_function(num: int):
    def color_print(text: str):
        print("\033[38;5;%dm %s \033[0m" % (num, text), end='')
    return color_print

# print all possible color combinations
# for a given number of colors
for i in range(256):
    color_function(i)(i)