import socket
import os
from _thread import *


def accept_packet(cnx):
    while True:
        try:
            data = cnx.recv(8186)  # receive request
            if data.decode():
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
                file = f.read().decode('ascii')
                f.close()
                packet = "{} 200 OK\r\n\r\n{}".format(version, file)
                cnx.send(packet.encode())
            else:
                packet = "{} 404 Not Found\r\n".format(version)
                cnx.send(packet.encode())

        elif msg[0].split()[0] == "POST":
            # filename = msg[0].split()[1][1:]  # get file name
            version = msg[0].split()[-1]  # get version
            f = open("data.txt", 'wb')  # Open in binary
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
while True:
    c, addr = s.accept()
    start_new_thread(accept_packet, (c,))
    threads += 1
