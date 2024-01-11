# find the large file (> 100M) then add its path to the file "largeFile.txt"

import os
import sys

def findLargeFile(path):
    path = os.path.abspath(path)

    dirList = []
    errorPath = []

    largeFileList_old = []
    largeFileList_new = []

    if os.path.exists("largeFile.txt"):
        with open ("largeFile.txt", "r") as f:
            for line in f.readlines():
                largeFileList_old.append(line.strip())
    else:
        with open ("largeFile.txt", "w") as f:
            pass

    if os.path.isfile(path):
        if os.path.getsize(path) > 100 * 1024 * 1024:
            if path not in largeFileList_old:
                largeFileList_new.append(path)
    elif os.path.isdir(path):
        dirList.append(path)
    else :
        errorPath.append(path)

    while len(dirList) > 0:
        path = dirList.pop()
        try:
            for file in os.listdir(path):
                filePath = os.path.join(path, file)

                if ( os.path.isfile(filePath) and
                     os.path.getsize(filePath) > 100 * 1024 * 1024 and
                     filePath not in largeFileList_old ):

                    largeFileList_new.append(filePath)

                elif os.path.isdir(filePath):
                    dirList.append(filePath)
                else:
                    errorPath.append(filePath)
        except:
            errorPath.append(path)
        
    if len(largeFileList_new) > 0:
        with open ("largeFile.txt", "a") as f:
            for file in largeFileList_new:
                print("large file:" + str(file))
                f.write(file + "\n")


    # ignore error path

    # if len(errorPath) > 0:
    #     print("Error path:")
    #     for path in errorPath:
    #         print("Error path:" + str(path))

    return errorPath

if __name__ == "__main__":

    defaultPath = os.getcwd()

    # findLargeFile(sys.argv[1])
    findLargeFile(defaultPath)