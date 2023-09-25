import socket
import keyboard
import os
import hashlib

esc_flg = False

def press_esc():
    global esc_flg
    esc_flg = True
keyboard.on_press_key('esc', press_esc)

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    if esc_flg:
        break
    file_path = input('Enter file path: ')
    # first send the file name and size to the server
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # get the md5 value of the file
    file_md5 = ""
    with open(file_path, 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        file_md5 = m.hexdigest()

    file_info = f"name:{file_name} & size:{file_size} & md5:{file_md5}"

    clientSocket.send(file_info.encode())
    # wait for the server to be ready
    while True:
        if clientSocket.recv(1024).decode() == "READY":
            break
        
    # then send the file
    with open(file_path, 'rb') as f:
        print("Sending file...")
        rest_size = file_size
        while True:
            data = f.read(1024)
            if not data:
                break
            rest_size -= len(data)
            print(f"Sending {file_size - rest_size}/{file_size} bytes...")
            # add the rest size before the data
            data = str(f"rest:{rest_size}&").encode() + data
            clientSocket.send(data)

    print("=" * 50)
    input("Do you want to continue? Press Enter to continue, or press Esc to exit...")