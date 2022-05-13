import socket
import os
from _thread import *


def ThreadedClient(cnx):
    print("start")
    # msg=''
    # cnx.send('Thank you for connecting\n'.encode())
    cnx.settimeout(15)
    while True:
        data = cnx.recv(2048)  # receive request
        msg = data.decode('ascii')
        msg = msg.split('\r\n')  # split header and filter empty strings
        msg = list(filter(None, msg))  # print("before", msg)
        print(msg)

        if len(msg) and len(msg[0].split()) > 2:
            print("after")
            if msg[0].split()[0] == "GET":
                print("get")
                filename = msg[0].split()[1][1:]  # get file name
                entries = os.listdir()  # entries in dir
                search = entries.count(filename)  # search for filename
                if search:
                    print("HTTP/1.0 200 OK\r\n")
                    cnx.send("HTTP/1.0 200 OK\r\n".encode())

                    f = open(filename, "rb")
                    #size = os.path.getsize(filename)
                    file = f.read()
                    cnx.send(file)
                    f.close()
                else:
                    print("HTTP/1.0 404 Not Found\r\n")
                    cnx.send("HTTP/1.0 404 Not Found\r\n".encode())

            elif msg[0].split()[0] == "POST":
                print("post")
                cnx.send('OK'.encode())
                filename = msg[0].split()[1][1:]  # get file name
                f = open(filename, 'wb')  # Open in binary
                #file = cnx.recv(8096)
                f.write(str.encode(msg[-1]))
                f.close()
        else:
            cnx.send("ERROR IN PACKET".encode())


# cnx.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
threads = 0
s.bind(('', 55555))
s.listen(5)

while True:
    c, addr = s.accept()
    start_new_thread(ThreadedClient, (c,))
    threads += 1
