import socket
from actions import *

HOST = 'localhost'
PORT = 3001

def connect_server(action_type):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        print("Connecting...")
        client.connect((HOST, PORT))
        client.sendall(action_type.encode("utf-8"))
        print("Information sent to server")

def enter():
    connect_server(ENTER)

def exit():
    connect_server(EXIT)

def emergency():
    connect_server(EMERGENCY)
