# input a file path, then print the md5 value of the file
import hashlib
import os

def get_md5(file_path: str) -> str:
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            m.update(data)
    return m.hexdigest()

if __name__ == "__main__":
    file_path = input("Enter file path: ")
    print(get_md5(file_path))