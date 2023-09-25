import os, sys
from os import path

os.chdir(sys.path[0])

PATH = "./test.txt"

# 输出此时的文件名，文件状态（是否关闭），访问方式
with open(PATH, "w") as file:
    if file:
        print(path.basename(PATH))
    else:
        print("the file is not found")

    print(bin(os.stat(PATH).st_mode))

file.close()
