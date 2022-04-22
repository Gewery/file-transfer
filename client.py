import socket
import os


def send_string(st):
    encoded_command = bytes(st, 'utf-8')
    kb = bytearray()
    for i in range(1024 - len(encoded_command)):
        kb.append(0)
    kb += encoded_command
    sock.send(kb)


def receive_string():
    st = bytearray(sock.recv(1024))
    while len(st) != 0 and st[0] == 0:
        st.remove(0)

    return st.decode('utf-8')


def download_file(server_location):
    send_string(server_location)
    response = receive_string()
    if response != 'ACK':
        print(response)
        return

    client_location = server_location[server_location.rfind('/') + 1:]
    if os.path.exists(client_location):
        print('File already exists, saving it as: ', end='')
        client_location, ext = client_location[:client_location.rfind('.')], client_location[
                                                                             client_location.rfind('.') + 1:]

        number = 1
        while os.path.exists(client_location + '_' + str(number) + '.' + ext):
            number += 1

        client_location += '_' + str(number) + '.' + ext

        print(client_location)

    f = open(client_location, 'wb+')
    number_of_kb = int(receive_string())

    for i in range(number_of_kb):
        f.write(sock.recv(1024))

    f.close()

    print('file ' + client_location + ' received')


port = 8800

address = input('Enter address to connect: ')

sock = socket.socket()
sock.connect((address, port))

while True:
    server_location = input('Enter the file location: ')
    download_file(server_location)
