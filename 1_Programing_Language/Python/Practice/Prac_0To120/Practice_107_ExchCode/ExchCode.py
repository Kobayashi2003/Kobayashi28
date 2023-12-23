import os
import sys
import argparse

def rebuild(filepath : str, encode="GBK", decode="Shift_JIS") -> None:
    if not os.path.exists(filepath):
        print("Invalid filepath")
        exit(1)
    old_filename = os.path.basename(filepath)

    new_filename = ""
    try:
        new_filename = old_filename.encode(encode).decode(decode)
    except:
        try:
            new_filename = old_filename.encode(encode).decode(decode, "ignore")
        except:
            print("Can't decode filename")
            exit(1)
        
    new_filepath = os.path.join(os.path.dirname(filepath), new_filename)
    if (os.path.exists(new_filepath) and 
        os.path.isfile(new_filepath) and
        os.path.getsize(new_filepath) > 0):
            print("File already exists")
            input("Press Enter to overwrite, or Ctrl+C to cancel")
    else:
        with open(new_filepath, "w", encoding=encode) as f:
            pass

    new_content = readfile(filepath, encode, decode)
    with open(new_filepath, "w", encoding=decode) as f:
        f.write(new_content)

    print(new_content)

    remove_ensure = input("Remove old file? (y/[n])") or "n"
    if remove_ensure == "y":
        os.remove(filepath)
    else:
        print("Old file is still there")


def recode_str(data: str, encode="GBK", decode="Shift_JIS") -> str:
    # return data.encode(encode).decode(decode)
    try:
        return data.encode(encode).decode(decode)
    except:
        try:
            return data.encode(encode).decode(decode, "ignore")
        except:
            return "Invalid string: " + data


def readfile(path: str, encode="GBK", decode="Shift_JIS") -> str:
    content = ""
    with open(path, "r", encoding=encode) as f:
        # return f.read().encode(encode).decode(decode)
        for line in f.readlines():
            try:
                content += line.encode(encode).decode(decode)
            except:
                try:
                    content += line.encode(encode).decode(decode, "ignore")
                except:
                    content += "Invalid line: " + line
    return content


if __name__ == "__main__":

    args = sys.argv
    if len(args) == 1:
        print("Invalid arguments")
        exit(1)

    if args[1] == "rebuild":
        if len(args) == 2:
            print("Please input the filepath")
            exit(1)
        filepath = args[2]
        if not os.path.exists(filepath):
            print("Invalid filepath")
            exit(1)
        else:
            rebuild(filepath)

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