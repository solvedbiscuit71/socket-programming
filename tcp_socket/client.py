import socket
import time
import array, struct

try:
    while True:
        payload = array.array('i', map(int, input('Enter your int[]: ').split(' ')))
        print(f"Received int[]: {payload}")
        payload = payload.tobytes()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
            con.connect(('localhost', 12000))
            con.send(struct.pack('i', len(payload)))
            con.send(payload)
            
            res = con.recv(4)
            resData, = struct.unpack('i', res)
            print(f'Server responds: {resData}')
except KeyboardInterrupt:
    print('Terminated')