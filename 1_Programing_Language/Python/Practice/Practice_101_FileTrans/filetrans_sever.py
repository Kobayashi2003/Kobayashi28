import socket
import os
import hashlib

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready!")

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Receiving file...")
    # first receive the file name and size from the client
    file_info = connectionSocket.recv(1024).decode()
    print(file_info)
    fileName = file_info.split(" & ")[0].split(":")[1]
    fileSize = file_info.split(" & ")[1].split(":")[1]
    fileMD5 = file_info.split(" & ")[2].split(":")[1]
    # wait for the client to be ready
    connectionSocket.send("READY".encode())

    # the file is received from the client and saved to the file to current directory
    data = b""
    with open(fileName, 'wb') as f:
        while True:
            print(data)
            data = connectionSocket.recv(1024)
            # devide the data into two parts: the rest size and the file data
            rest_size = int(data.split(b"&")[0].split(b":")[1])
            data = data.split(b"&")[1:]
            for d in data:
                f.write(d)
            if rest_size == 0:
                break

    print("File received successfully!")

    # check the md5 value of the file
    file_md5 = ""
    with open(fileName, 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        file_md5 = m.hexdigest()
    if file_md5 == fileMD5:
        print("The file is not corrupted!")

    connectionSocket.close()
        