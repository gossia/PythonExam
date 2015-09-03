import socket
import datetime

host = '0.0.0.0'
port = 51235
size = 1024


try:
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
except socket.error as msg:
    print('Exception: ', msg)

raport_no = 1

while True:
    try:
        c, addr = s.accept()
        print('Got connection from', addr)
        data = datetime.datetime.now().date()
        filename = "raport-" + str(raport_no) + "_" + str(data) + ".txt"
        f = open(filename,'wb')
        data = c.recv(size)
        while data:
            print("Receiving data...")
            f.write(data)
            data = c.recv(size)
        f.close()
        print("Done receiving")
        raport_no += 1
        c.close()
    except socket.error as msg:
        c.close()
        print('Exception: ', msg)


