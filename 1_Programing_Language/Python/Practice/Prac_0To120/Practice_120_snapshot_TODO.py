import os

# find all the files in the current directory and subdirectories
# out put their paths and size to a snapshot file

def snapshot():
    cwd = os.getcwd()
    snapshotFile = open('snapshot', 'w')
    for root, dirs, files in os.walk(cwd):
        for file in files:
            path = os.path.join(root, file)
            size = os.path.getsize(path)
            try:
                snapshotFile.write(f"{path}: {size}\n")
            except UnicodeEncodeError:
                snapshotFile.write("{UnicodeEncodeError}\n")
    snapshotFile.close()


def compareSnapshots(old, new):
    # read the file with gbk encoding
    oldFile = open(old, 'r', encoding='gbk')
    newFile = open(new, 'r', encoding='gbk') 
    oldLines = oldFile.readlines()
    newLines = newFile.readlines()
    oldFile.close()
    newFile.close()
    oldFiles = {}
    newFiles = {}
    for line in oldLines:
        try:
            path, size = line.split(': ')
            oldFiles[path] = int(size)
        except:
            pass
    for line in newLines:
        try:
            path, size = line.split(': ')
            newFiles[path] = int(size)
        except:
            pass
    # if the file is in the old snapshot but not in the new one, or if the file is in both but the size is dropped, print it in green
    # if the file is in the new snapshot but not in the old one, or if the file is in both but the size is increased, print it in red
    for path in oldFiles:
        if path not in newFiles:
            print(f"\033[32m{path}: {oldFiles[path]} was deleted\033[0m")
        elif newFiles[path] < oldFiles[path]:
            print(f"\033[32m{path} was shrunk from {oldFiles[path]} to {newFiles[path]}\033[0m")
    for path in newFiles:
        if path not in oldFiles:
            print(f"\033[31m{path}: {newFiles[path]} was added\033[0m")
        elif newFiles[path] > oldFiles[path]:
            print(f"\033[31m{path} was grown from {oldFiles[path]} to {newFiles[path]}\033[0m")

        
# snapshot()
compareSnapshots('D:/Program/Code/Temp/old', 'D:/Program/Code/Temp/new')
