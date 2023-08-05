import os
import os.path

while True:
    rootdir = input("请输入遍历文件夹的绝对路径：(q 退出)")
    if rootdir == 'q':
        break
    if not (os.path.exists(rootdir)):
        print("输入的路径不存在，请重新输入!")
        continue
    for parent, dirnames, filenames in os.walk(rootdir):
        # 三个参数：分别返回 1. 父目录 2. 所有文件名字（不含路径） 3. 所有文件名字
        for dirname in dirnames:
            print("parent is: " + parent)
            print("dirname is:" + dirname)

        for filename in filenames:
            print("parent is: " + parent)
            print("filename is: " + filename)
            print("the full name of the file is: " + os.path.join(parent, filename))
