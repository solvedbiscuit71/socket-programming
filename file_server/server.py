import os
import socket

PUT=b'\x00'
GET=b'\x01'
LIST=b'\x02'

SUCCESS=b'\x00'
ERROR=b'\x01'

serverAddress = ('', 12000)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen()

print("Server listening at 12000")

def does_exists(name):
    return os.path.exists(name) and os.path.isfile(name)

if not os.path.exists('store'):
    os.mkdir('store')

try:
    while True:
        con, addr = serverSocket.accept()
        print(f"[LOG] Established TCP connection with {addr}")

        request = con.recv(1)
        match request:
            case b"\x00": # PUT
                try:
                    buf = con.recv(1)
                    while buf[-1] != 0:
                        buf += con.recv(1)

                    filename = str(buf[:-1], 'ascii')
                    with open('store/'+filename, 'wb') as file:
                        while len(buf := con.recv(1024)) > 0:
                            file.write(buf)
                    con.send(SUCCESS)
                    print(f"[LOG] Success: {filename} written")
                except Exception as e:
                    con.send(ERROR)
                    print(f"[LOG] Error: {e}")
                finally:
                    print(f"[LOG] Connection closed with {addr}")
                    con.close()

            case b"\x01": # GET
                try:
                    buf = con.recv(1)
                    while buf[-1] != 0:
                        buf += con.recv(1)

                    filename = str(buf[:-1], 'ascii')
                    if not does_exists('store/'+filename):
                        raise FileNotFoundError

                    con.send(SUCCESS)
                    with open('store/'+filename, 'rb') as file:
                        while len(chunk := file.read(1024)) > 0:
                            sentByte = con.send(chunk)
                    con.shutdown(socket.SHUT_WR)
                    print(f"[LOG] Success: {filename} sent")
                except FileNotFoundError:
                    con.send(ERROR)
                    print(f"[LOG] FileNotFound {filename}")
                except:
                    con.send(ERROR)
                    print(f"[LOG] Error")
                finally:
                    print(f"[LOG] Connection closed with {addr}")
                    con.close()

            case b'\x02': # LIST
                try:
                    if not os.path.exists('store'):
                        os.mkdir('store')

                    con.send(SUCCESS)
                    data = b'\x00'.join(map(lambda x: bytes(x, 'ascii'), os.listdir('store')))
                    con.send(data + b'\x00')
                    con.shutdown(socket.SHUT_WR)
                    print(f"[LOG] Succes: listdir sent")
                except:
                    con.send(ERROR)
                    print(f"[LOG] Error")
                finally:
                    print(f"[LOG] Connection closed with {addr}")
                    con.close()

except KeyboardInterrupt:
    print('Terminating...')

finally:
    serverSocket.close()