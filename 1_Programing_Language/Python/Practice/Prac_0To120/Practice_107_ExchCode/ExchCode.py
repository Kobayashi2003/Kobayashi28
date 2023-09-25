import os
import sys

def rename(workpath : str, encode="GBK", decode="Shift_JIS") -> None:
    CurrentPath = os.getcwd()
    os.chdir(workpath)
    for path in os.listdir():
        if os.path.isdir(path):
            rename(path, encode, decode)
        else :
            try:
                os.rename(path, path.encode(encode).decode(decode))
            except:
                print("Invalid file name: " + path)
    try:
        os.chdir(CurrentPath)
    except:
        print("Invalid workpath: " + workpath)


def recode_str(data: str, encode="GBK", decode="Shift_JIS") -> str:
    return data.encode(encode).decode(decode)


def readfile(path: str, encode="GBK", decode="Shift_JIS") -> str:
    with open(path, "r", encoding=encode) as f:
        return f.read().encode(encode).decode(decode)


if __name__ == "__main__":

    args = sys.argv
    if len(args) == 1:
        print("Invalid arguments")
        exit(1)

    if args[1] == "rename":
        if len(args) == 2:
            print("Please input the workpath")
            exit(1)
        workpath = args[2]
        if not os.path.exists(workpath):
            print("Invalid workpath")
            exit(1)
        rename(workpath)
    elif args[1] == "recode":
        str = args[2:]
        for i in range(len(str)):
            str[i] = recode_str(str[i])
        print(str)
    elif args[1] == "read":
        if len(args) == 2:
            print("Please input the filepath")
            exit(1)
        filepath = args[2]
        if not os.path.exists(filepath):
            print("Invalid filepath")
            exit(1)
        print(readfile(filepath))

    else :
        print("Invalid arguments")

    pass    