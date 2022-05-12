# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

server_address = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            respond = "HTTP/1.1 200 OK\r\n\r\nHello, World!".encode('ascii')
            conn.sendall(respond)

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# server_socket.bind(server_address)
#
# print("server socket info ", server_socket)
# print("server waiting")
#
# packet = server_socket.recvfrom(4096)
#
# data, client_address = packet
# print("server in :", data)
#
# server_socket.sendto(data,client_address)


# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# client_socket.sendto(b"hello world", server_address)
#
# print("client done")
#
# server_packet = client_socket.recvfrom(2048)
#
# print("client data : ", server_packet)
