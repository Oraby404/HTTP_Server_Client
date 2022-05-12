import socket
import os.path

file = open('input.txt', 'r')
commands = file.readlines()
file.close()

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

    file_exists = os.path.exists(file_name)

    if file_exists:  # found in cache
        if args[0] == "GET":
            print("File Found On Local Cache!\n")
            file = open(file_name, 'r')
            file_data = file.read()
            file.close()
            print(file_data)

    else:  # contact server

        if args[0] == "GET":
            request = "{} {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(args[0], url, HOST).encode('ascii')
        else:
            file = open(file_name, 'r')
            file_data = file.read()
            file.close()
            request = "{} HTTP/1.1\r\nHost: {}\r\n\r\n{}".format(args[0], HOST, file_data).encode('ascii')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(request)
            data = s.recv(8196)
            s.close()

            decoded_data = data.decode('ascii')
            info = decoded_data.split('\r\n\r\n')
            response = info[0]
            print(response, '\n')

            if args[0] == "GET":
                received_file = info[1]
                file = open(file_name, 'w')
                file.write(received_file)
                file.close()
                print(received_file)

    print("=========================================================================")
