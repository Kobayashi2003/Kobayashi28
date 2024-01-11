# 编写一个命令或脚本递归的查找文件夹中最近使用的文件。更通用的做法，你能够按照最近的使用时间列出文件吗？

find . -type f -mmin -60 -print0 | xargs -0 ls -lt | head -10 

