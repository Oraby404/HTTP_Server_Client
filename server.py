import socket
import os
from _thread import *
import random


def accept_packet(cnx):
    thread = 1
    while True:
        try:
            data = cnx.recv(8186)  # receive request
            if data.decode():
                print("Request number :", thread ,"\nPACKET :\n", data.decode('ascii'), "==============================")
                thread += 1
                start_new_thread(ThreadedClient, (cnx, data,))
        except:
            pass


def ThreadedClient(cnx, data):
    cnx.settimeout(15)
    msg = data.decode('ascii')
    msg = msg.split('\r\n')  # split header and filter empty strings
    msg = list(filter(None, msg))

    # check if packet format is correct get/post line with mandatory fields
    if len(msg) and len(msg[0].split()) > 1:
        if msg[0].split()[0] == "GET":
            filename = msg[0].split()[1]  # get file name
            version = msg[0].split()[-1]  # get version
            entries = os.listdir()  # entries in dir
            search = entries.count(filename)  # search for filename

            if search:  # if file is on server
                f = open(filename, "rb")
                file = f.read()
                f.close()

                packet = "{} 200 OK\r\n\r\n".format(version)
                packet = packet.encode() + file
                cnx.send(packet)
            else:
                packet = "{} 404 Not Found\r\n".format(version)
                cnx.send(packet.encode())

        elif msg[0].split()[0] == "POST":
            # filename = msg[0].split()[1][1:]  # get file name
            version = msg[0].split()[-1]  # get version
            f = open(str(random.randint(0, 20)) + ".txt", 'wb')  # Open in binary
            try:
                f.write(str.encode(msg[-1]))
                packet = "{} 200 OK".format(version)
                cnx.send(packet.encode())
            except:
                cnx.send("{} 400 Bad Request".format(version).encode())

            f.close()
    else:
        cnx.send("PACKET NOT VALID".encode())
        cnx.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
threads = 0
s.bind(('', 65432))
s.listen(5)
i = 0
while True:
    c, addr = s.accept()
    if c:
        # socket timeout
        s.settimeout(15)
        print("connection number : ", i)
        i = i + 1
        start_new_thread(accept_packet, (c,))
    threads += 1

# import socket
#
# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
#
# server_address = (HOST, PORT)
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind(server_address)
#     s.listen()
#     s.settimeout(10)
#
#     while True:
#         conn, addr = s.accept()
#         print(f"Connected by {addr}")
#         data = conn.recv(1024)
#         decoded_data = data.decode('ascii')
#         print('\n', decoded_data, '\n')
#         respond = "HTTP/1.1 200 OK\r\n\r\nHello, World! \n\n{}".format(decoded_data).encode('ascii')
#         conn.sendall(respond)
