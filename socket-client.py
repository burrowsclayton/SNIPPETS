#!/usr/bin/env python3

import socket
import datetime

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

cnt = 0

while True:
    cnt = cnt + 1
    body = "Client1: {}    {}".format(datetime.datetime.now(), cnt).encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(body)
        data = s.recv(1024)
        print('Received', repr(data.decode()))
