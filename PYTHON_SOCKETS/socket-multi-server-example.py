

import sys
import socket
import selectors
import types
import pickle

from Test import Test
import MakeBytes

sel = selectors.DefaultSelector()

def example(data):
    obj = MakeBytes.deserialize(data.inb)
    obj.execute()
    obj.add_data("hello from the server!")
    return MakeBytes.serialize(obj)

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
            data.inb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()

        # test out the pickle
        data.outb = example(data)

    if mask & selectors.EVENT_WRITE:

        if data.outb:
            print("echoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


#if len(sys.argv) != 3:
#    print("usage:", sys.argv[0], "<host> <port>")
#    sys.exit(1)

#host, port = sys.argv[1], int(sys.argv[2])
host = '127.0.0.1'  # Standard loopback interface address (localhost)
port = 65432        # Port to listen on (non-privileged ports are > 1023)

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except Exception as e:
    print(e)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
