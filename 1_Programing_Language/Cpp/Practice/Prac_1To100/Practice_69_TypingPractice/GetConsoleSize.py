# get the console size, and save the size to ConsoleSize file

import os
import time


def getConsoleSize():
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines
    return width, height


def saveConsoleSize(width, height):
    with open("ConsoleSize", "w+") as f:
        f.write(str(width) + "\n" + str(height))


if __name__ == "__main__":
    # check if there is a file name "ENDFLAG" in the current directory, if yes, first delete it
    if os.path.exists("ENDFLAG"):
        os.remove("ENDFLAG")
    while True: 
        # then check if there is a file name "ENDFLAG" in the current directory, if yes, end the loop
        if os.path.exists("ENDFLAG"):
            break
        width, height = getConsoleSize()
        saveConsoleSize(width, height)
        # print("width: " + str(width) + " height: " + str(height))
        # sleep 0.1 second
        time.sleep(0.1)
    # delete the ENDFLAG and ConsoleSize file
    os.remove("ENDFLAG")
    os.remove("ConsoleSize")
