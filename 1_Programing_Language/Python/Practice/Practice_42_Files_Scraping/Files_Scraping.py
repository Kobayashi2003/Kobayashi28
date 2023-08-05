# 将文件目录下的文件按照修改时间的顺序按 1 到 n 的依次进行重命名

import os

PATH = os.path.abspath(os.getcwd()) # 首先抓取当前文件所在的目录并将其规范化
with open( os.path.abspath(os.path.join(PATH, 'FILES')), 'w' ) as f:

    for parent, dirnames, filenames in os.walk(PATH, topdown=True, onerror=None, followlinks=False): # 遍历当前文件夹 topdown为 True， 则优先遍历 top 目录 oneerror 需要一个 callable 对象，当 wald 产生异常时，会被调用。 followlinks 为 True，则会遍历目录下的目录，默认情况下为 False。walk 每次遍历返回的对象都是一个三元组(root, dirs, files)， 其中 root 为当前正在遍历的这个文件夹本身的地址；dirs 是一个列表，内容是该文件夹中所有目录的名字（不包括子目录）；files 同样是列表，内容是该文件夹中所有的文件（不包括子目录）
        files_created_time = []
        files_table = {}

        for filename in filenames:
            file_path = os.path.abspath( os.path.join(parent, filename) ) # 将文件所在的文件夹所在的路径与该文件名结合成该文件的绝对路径，并将其规范化
            file_created_time = os.path.getmtime(file_path) # 取用该文件的最后修改时间
            # print(f"{filename} : {file_created_time}")

            files_table[file_created_time] = filename
            files_created_time.append(file_created_time)

        # print('='*50)
        # files_created_time.sort()
        # print(files_created_time)
        # print(files_table)
        print("="*50)
        for time in files_created_time:
            print(files_table.get(time, None))
            f.write(files_table.get(time, None) + "\n")
            
