import socket
import os
import time

# read list of commands

file = open('input.txt', 'r')
commands = file.readlines()
file.close()

# load cache from log file

cache = set()

file = open('cache.txt', 'r')
cache_list = file.readlines()
file.close()

for line in cache_list:
    line = line.split('\n')
    if os.path.exists(line[0]):
        cache.add(line[0])

print(cache, '\n')

# process each command in the input file

for command in commands:
    args = command.split(' ')
    args = [i.strip() for i in args]
    if len(args) == 3:
        args.append('80')

    HOST = args[2]
    PORT = int(args[3])
    server_address = (HOST, PORT)

    url = args[1]
    path = url.split('/')
    file_name = path[len(path) - 1]

    cache_file_name = str(HOST + '_' + file_name)
    file_exists = cache_file_name in cache

    if file_exists and args[0] == "GET":  # found in cache
        print("File Found On Local Cache!\n")
        file = open(cache_file_name, 'rb')
        file_data = file.read()
        file.close()
        print(cache_file_name, '\n')

    else:  # contact server

        if args[0] == "GET":
            request = "{} {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(args[0], url, HOST).encode('ascii')
        else:
            file = open(file_name, 'rb')
            file_data = file.read()
            file.close()
            packet = "{} {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(args[0], url, HOST)
            request = packet.encode('ascii') + file_data

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(request)

            data = b''
            i = 1
            while True:
                new_data = s.recv(10240)
                time.sleep(0.000000001)
                data += new_data

                if len(data) < 10240 * i:
                    break

                i += 1

            s.close()

            # decoded_data = data.decode('ascii')
            info = data.split(b'\r\n\r\n')
            response = info[0].decode('ascii')
            status = response.split('\r\n')
            print(request.decode('ascii'), '\n', response, '\n')

            if args[0] == "GET" and status[0] == "HTTP/1.1 200 OK":
                received_file = info[1]
                file = open(cache_file_name, 'wb')
                file.write(received_file)
                file.close()

                cache.add(cache_file_name)
                file = open('cache.txt', 'a')
                file.write(cache_file_name + '\n')
                file.close()

                # print(received_file)
    print("=========================================================================")
