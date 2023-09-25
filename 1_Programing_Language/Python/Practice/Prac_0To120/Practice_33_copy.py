# 文件读写案列 -- 复制文件

# 打开文件

file_read = open("README")
file_write = open("README_COPY", 'w')


# 读写
text = file_read.read()
file_write.write(text)

# 关闭文件
file_read.close()
file_write.close()
