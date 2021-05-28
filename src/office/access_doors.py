from realtcp import *
from gpio import *
import time

ENTRY_BUTTON = 0
ENTRY_DOOR = 2
ENTRY_LED = 4

EXIT_BUTTON = 1
EXIT_DOOR = 3
EXIT_LED = 5


SERVER_IP = "localhost"
SERVER_PORT = 3001

ENTER = "ENTER"
EXIT = "EXIT"

client = RealTCPClient()

connected = False


def onTCPConnectionChange(type):
    global connected
    print("connection changed: " + str(type))
    connected = int(type) > 0


def isLocked(input):
    state = customRead(input)
    lock = int(state[2])
    return lock == 1


def isOpen(input):
    state = customRead(input)
    open = int(state[0])
    return open == 1


def lockDoor(input):
    customWrite(input, "0,1")


def openDoor(input):
    customWrite(input, "1,0")


def buttonPressed(input):
    THRESHOLD = 100
    state = int(digitalRead(input))
    return state > THRESHOLD


def ledOn(input):
    analogWrite(input, 1023)


def ledOff(input):
    analogWrite(input, 0)


def openEntryDoor():
    ledOn(ENTRY_LED)
    openDoor(ENTRY_DOOR)


def closeEntryDoor():
    lockDoor(ENTRY_DOOR)
    ledOff(ENTRY_LED)


def openExitDoor():
    ledOn(EXIT_LED)
    openDoor(EXIT_DOOR)


def closeExitDoor():
    lockDoor(EXIT_DOOR)
    ledOff(EXIT_LED)


def entryDoorSequence():
    openEntryDoor()
    time.sleep(5)
    closeEntryDoor()


def exitDoorSequence():
    openExitDoor()
    time.sleep(5)
    closeExitDoor()


def entry():
    entryDoorSequence()
    time.sleep(0.5)
    exitDoorSequence()


def exit():
    exitDoorSequence()
    time.sleep(0.5)
    entryDoorSequence()


def main():
    while True:
        if not connected:
            client.connect(SERVER_IP, SERVER_PORT)
            client.onConnectionChange(onTCPConnectionChange)
        lockDoor(ENTRY_DOOR)
        lockDoor(EXIT_DOOR)
        if buttonPressed(ENTRY_BUTTON):
            client.send(ENTER)
            entry()
        if buttonPressed(EXIT_BUTTON):
            client.send(EXIT)
            exit()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
