
import sys
import socket
import selectors
import types
import pickle

class Connection:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sel = selectors.DefaultSelector()
        self.sock = self.connect()
        self.data = None # see register(obj)


    def connect(self):
        server_addr = (self.host, self.port)
        print("starting connection", connid, "to", server_addr)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        return sock

    def clean(self):
        try:
            self.sock.close()
        finally:
            self.sel.close()

    def __pickle(self, obj, header_size=10):
        msg = pickle.dumps(d)
        return bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg

    def register(self, obj):

        # register read/write events and the data that will be written
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.data = types.SimpleNamespace(
            recv_total=0,
            outb=self.__pickle(obj),
            inb=b""
        )
        self.sel.register(self.sock, events, data=data)

