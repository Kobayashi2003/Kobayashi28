# get a string, then print the md5 value of the string
import hashlib

def get_md5(string: str) -> str:
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()

if __name__ == "__main__":
    string = input("Enter a string: ")
    print(get_md5(string))