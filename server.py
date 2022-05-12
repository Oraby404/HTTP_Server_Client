# import socket
# import os
# from _thread import *
#
#
# def ThreadedClient(cnx):
#     cnx.timeout(15)
#     while True:
#         data = cnx.recv(1024)
#
#         msg = (str(data)[2:-1].split('\\r\\n'))  # split header and filter empty strings
#         msg = list(filter(None, msg))
#
#         print(msg)
#
#         if len(msg) > 1:
#             if msg[0].split()[0] == "GET":
#                 filename = msg[0].split()[1][1:]  # get file name
#                 entries = os.listdir()  # entries in dir
#                 search = entries.count(filename)  # search for filename
#                 if search:
#                     cnx.send("HTTP/1.0 200 OK\r\n".encode())
#                     f = open(filename, "rb")
#
#                     file = f.read(1024)
#                     while file:
#                         cnx.send(file)
#                         file = f.read(1024)
#                 else:
#                     cnx.send("HTTP/1.0 404 Not Found\r\n".encode())
#
#             elif msg[0].split()[0] == "POST":
#                 filename = msg[0].split()[1][1:]  # get file name
#                 cnx.send('OK'.encode())
#
#                 f = open(filename, 'wb')  # Open in binary
#                 while True:
#                     file = cnx.recv(1024)
#                     f.write(file)
#                     if not file:
#                         break
#                 f.close()
#         else:
#             cnx.send("ERROR".encode())
#
#         if not data:  # when client end cnx
#             print('CLIENT ENDED CONNECTION')
#             break
#     cnx.close()
#
# ###########################################################################
#
#
# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
# server_address = (HOST, PORT)
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# threads = 0
# s.bind(server_address)
# s.listen(20)
#
# while True:
#     conn, addr = s.accept()
#     start_new_thread(ThreadedClient, (conn,))
#     threads += 1


import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

server_address = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind(server_address)
    s.listen()
    s.settimeout(10)

    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        decoded_data = data.decode('ascii')
        respond = "HTTP/1.1 200 OK\r\n\r\nHello, World! \n\n{}".format(decoded_data).encode('ascii')
        conn.sendall(respond)
