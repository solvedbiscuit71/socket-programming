import os
import socket

PUT=b'\x00'
GET=b'\x01'
LIST=b'\x02'

SUCCESS=b'\x00'
ERROR=b'\x01'

serverAddress = ('localhost',12000)

def does_exists(name):
    return os.path.exists(name) and os.path.isfile(name)

while True:
    cmd = input("> ")
    if len(cmd) == 0:
        continue
    cmd = cmd.split(' ')
    if len(cmd) not in (1,2):
        print("Invalid command")
        continue
    match cmd[0].upper():
        case 'PUT':
            filename = cmd[1]
            if not does_exists(filename):
                print("File doesn't exists")
                continue
            
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect(serverAddress)
            header = PUT + bytes(filename, 'ascii') + b'\x00'
            con.send(header)
            with open(filename, 'rb') as file:
                while len(chunk := file.read(1024)) > 0:
                    sentByte = con.send(chunk)
            con.shutdown(socket.SHUT_WR)
            status = con.recv(1)
            if status == SUCCESS:
                print("[LOG] Success")
            else:
                print("[LOG] Error")
            con.close()
            
        case 'GET':
            filename = cmd[1]
            
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect(serverAddress)
            header = GET + bytes(filename, 'ascii') + b'\x00'
            con.send(header)
            con.shutdown(socket.SHUT_WR)
            status = con.recv(1)
            if status == SUCCESS:
                with open(filename, 'wb') as file:
                    while len(buf := con.recv(1024)) > 0:
                        file.write(buf)
                print("[LOG] Success")
            else:
                print("[LOG] Error")
            con.close()

        case 'LIST':
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect(serverAddress)
            con.send(LIST)
            con.shutdown(socket.SHUT_WR)
            status = con.recv(1)
            if status == SUCCESS:
                print("[LOG] Sucess")
                buf = b''
                while len(buf := buf+con.recv(256)) > 0:
                    while buf.find(0) != -1:
                        filename = str(buf[:buf.find(0)], 'ascii')
                        if filename:
                            print(filename)
                        buf = buf[buf.find(0)+1:]
            else:
                print("[LOG] Error")
            con.close()
        case 'QUIT' | 'CLOSE' | 'EXIT':
            break
        case _:
            print("Invalid command")
    print()
