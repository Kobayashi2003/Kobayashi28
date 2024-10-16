import socket 

HOST = 'localhost'
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b'Hello, world', (HOST, PORT))
    data, addr = s.recvfrom(1024)
    print('Received', repr(data))