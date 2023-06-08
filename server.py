import socket
import os


def send_file(file_location):
    f = open(file_location, 'rb')
    to_send = []
    chunk = f.read(1024)
    while chunk:
        to_send.append(chunk)
        chunk = f.read(1024)

    send_string(str(len(to_send)))

    total_chunks = len(to_send)
    chunks_sent = 0
    for kb in to_send:
        con.send(kb)
        chunks_sent += 1
        if chunks_sent % 100 == 0:
            print('sent ' + str(chunks_sent) + ' / ' + str(total_chunks) + ' chunks')

    f.close()

    print('file ' + file_location + ' sent')


def receive_string():
    st = bytearray(con.recv(1024))
    while len(st) != 0 and st[0] == 0:
        st.remove(0)

    return st.decode('utf-8')


def send_string(str):
    print('sending string to client:', str)
    encoded_command = bytes(str, 'utf-8')
    kb = bytearray()
    for i in range(1024 - len(encoded_command)):
        kb.append(0)
    kb += encoded_command
    con.send(kb)  # send command with 0-bytes in the beginning)


port = 8800

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
s.listen()

con, addr = s.accept()
print(str(addr) + ' connected')

while True:
    file_location = receive_string()
    print('Requested file: ', file_location)

    if not os.path.exists(file_location):
        error = 'File ' + file_location + ' does not exists'
        send_string('Error: ' + error)
    else:
        send_string('ACK')
        send_file(file_location)
        print('file ' + file_location + ' sent')



