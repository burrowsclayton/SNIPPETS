
# Python3.7+
import socket
import selectors
import types
import datetime
from sqlite3 import connect

class DataManager:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()
        self.cnt = 0

    def write(self, strng):
        self.cnt += 1

        tup = (strng, datetime.datetime.now(), self.cnt)

        self.cur.execute("insert into socket(response, time, cnt) values(?, ?, ?)", tup)
        self.con.commit()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask, cur):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)

            strng = str(data.outb)
            dm.write(strng)

            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

sel = selectors.DefaultSelector()

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


sel = selectors.DefaultSelector()
# ...
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print('listening on', (HOST, PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


with connect('socket.db') as con:
    dm = DataManager(con)
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask, dm)
