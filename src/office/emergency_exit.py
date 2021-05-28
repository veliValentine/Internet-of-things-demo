from realtcp import *
from gpio import *


SERVER_IP = "localhost"
SERVER_PORT = 3001

EMERGENCY = "EMERGENCY"

DOOR = 0
SIREN = 1

client = RealTCPClient()


def onTCPConnectionChange(type):
    print("connection changed: " + str(type))


def onTCPReceive(data):
    print("received: " + data)


def isOpen():
    state = customRead(DOOR)
    open = int(state[0])
    return open == 1


def isLocked():
    state = customRead(DOOR)
    lock = int(state[2])
    return lock == 1


def sirenOn():
    customWrite(SIREN, "1")


def sirenOff():
    customWrite(SIREN, "0")


def main():
    client.onConnectionChange(onTCPConnectionChange)
    client.onReceive(onTCPReceive)

    client.connect(SERVER_IP, SERVER_PORT)
    sent = False
    while True:
        if isOpen():
            sirenOn()
            if not sent:
                client.send(EMERGENCY)
                sent = True
        else:
            sirenOff()
            sent = False


if __name__ == "__main__":
    main()
