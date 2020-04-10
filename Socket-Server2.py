
# Python3.7+
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

listen_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(10)

print(f'Serving HTTP on port {PORT} ...')
cnt = 0

while True:
    cnt = cnt + 1
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024).decode()
    print("\n", request_data, "\n")
    request_data = "{}\tServer-Count: {}".format(request_data, cnt).encode()

    client_connection.sendall(request_data)
    client_connection.close()
