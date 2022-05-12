import socket
import os
from _thread import *


def ThreadedClient(cnx):
    cnx.timeout(15)
    while True:
        data = cnx.recv(1024)

        msg = (str(data)[2:-1].split('\\r\\n'))  # split header and filter empty strings
        msg = list(filter(None, msg))

        print(msg)

        if len(msg) > 1:
            if msg[0].split()[0] == "GET":
                filename = msg[0].split()[1][1:]  # get file name
                entries = os.listdir()  # entries in dir
                search = entries.count(filename)  # search for filename
                if search:
                    cnx.send("HTTP/1.0 200 OK\r\n".encode())
                    f = open(filename, "rb")

                    file = f.read(1024)
                    while file:
                        cnx.send(file)
                        file = f.read(1024)
                else:
                    cnx.send("HTTP/1.0 404 Not Found\r\n".encode())

            elif msg[0].split()[0] == "POST":
                filename = msg[0].split()[1][1:]  # get file name
                cnx.send('OK'.encode())

                f = open(filename, 'wb')  # Open in binary
                while True:
                    file = cnx.recv(1024)
                    f.write(file)
                    if not file:
                        break
                f.close()
        else:
            cnx.send("ERROR".encode())

        if not data:  # when client end cnx
            print('CLIENT ENDED CONNECTION')
            break
    cnx.close()


s = socket.socket()
threads = 0
s.bind(('', 65432))
s.listen(20)

while True:
    c, addr = s.accept()
    start_new_thread(ThreadedClient, (c,))
    threads += 1
