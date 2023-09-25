import os,sys
from os import path

os.chdir(sys.path[0])

file_path = "hei.txt"

file = open(file_path, "w")
file.write("hello")
file.close()

file_read = open(file_path, "r")
contents = file_read.readlines()
print(contents)
file_read.close()

os.remove(file_path)