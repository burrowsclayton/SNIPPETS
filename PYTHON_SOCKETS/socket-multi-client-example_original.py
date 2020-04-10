import sys
import socket
import selectors
import types
import pickle

from Test import Test

def start_connections(messages, host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print("starting connection", connid, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            #msg_total=sum(len(m) for m in messages),
            msg_total=len(messages),
            recv_total=0,
            messages=[messages],
            outb=messages,
            inb=b""
        )
        sel.register(sock, events, data=data)


def service_connection(key, mask, dict_tracker):
    print(dict_tracker)
    dict_tracker['count'] += 1
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        print("\nEVENT_READ")
        if recv_data:
            print("received", repr(recv_data), "from connection", data.connid)
            data.recv_total += len(recv_data)
            data.inb += recv_data
        if not recv_data or data.recv_total >= data.msg_total:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        #if not data.outb and data.messages:
        #    data.outb = data.messages.pop(0)
        if data.outb:
            print("\nEVENT_WRITE")
            print("sending", repr(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]



def sendPickle(obj, host, port, num_conns):

    sel = selectors.DefaultSelector()
        
    start_connections(host, int(port), int(num_conns))
    dict_tracker['count'] = 1
    dict_tracker['contents'] = ob
    try:
        while True:
            events = sel.select(timeout=1)
            if events:
                for key, mask in events:
                    service_connection(key, mask, dict_tracker)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()



#if len(sys.argv) != 4:
#    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
#    sys.exit(1)

#host, port, num_conns = sys.argv[1:4]

host = '127.0.0.1'  # Standard loopback interface address (localhost)
port = 65432        # Port to listen on (non-privileged ports are > 1023)
num_conns = 1

sendPickle(Test(), host, port, num_conns)
