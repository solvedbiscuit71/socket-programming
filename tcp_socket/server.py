import socket
import array, struct
import time
import threading

def compute_sum(con):
    print(f'Connection accepted {addr[1]}')
    with con:
        time.sleep(2)
        req = con.recv(4)
        size, = struct.unpack('i', req)
        print(f'[LOG] size = {size}')
        req = con.recv(size)
        nums = array.array('i', req)
        print(f'[LOG] nums = {nums}')
        
        res = sum(nums) % (2**31)
        print(f'[LOG] response = {res}')
        time.sleep(2)
        con.send(struct.pack('i', res))

    print('Connection closed')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.bind(('', 12000))
    serverSocket.listen()
    print('server listening at 12000')
    
    try:
        while True:
                con, addr = serverSocket.accept()
                handler = threading.Thread(target=compute_sum, args=(con,))
                handler.start()
    except KeyboardInterrupt:
        print('Terminate')