import socket
import selectors
import types

from actions import *
from counter import Personel_Counter

HOST = 'localhost'
PORT = 3001

personel_in_building = Personel_Counter()


def accept_wrapper(sock):
    connection, address = sock.accept()
    print("Accepted connection from: ", address)
    connection.setblocking(False)
    data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
    events = selectors.EVENT_READ
    sel.register(connection, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            handle_action(recv_data.decode("utf-8").strip().upper())
        else:
            print("Closing connection to: ", data.addr)
            sel.unregister(sock)
            sock.close()


def handle_action(action):
    if action == ENTER:
        return personel_in_building.enter()
    if action == EXIT:
        return personel_in_building.exit()
    if action == EMERGENCY:
        return personel_in_building.emergency()
    print("Could not process action")


sel = selectors.DefaultSelector()
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.bind((HOST, PORT))
serv_sock.listen()
print("listening on:", (HOST, PORT))
serv_sock.setblocking(False)
sel.register(serv_sock, selectors.EVENT_READ, data=None)
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
