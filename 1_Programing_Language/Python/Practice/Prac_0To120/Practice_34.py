# 大文件复制

# 打开文件

file_read = open("README")
file_write = open("README_COPY", 'w')


# 读写
while True:
    text = file_read.readline()

    if not text:
        break

    file_write.write(text)

# 关闭文件
file_read.close()
file_write.close()
