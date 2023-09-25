import os, sys
from os import path

os.chdir(sys.path[0])

file_path = "test.txt"

with open(file_path, '+w') as file:
    file.write("kobayashi")
    file.seek(0)
    contents = file.read(11)
    print(contents)
    print(path.abspath(os.getcwd() + "/test.txt"))