from realtcp import *
from gpio import *
from time import *

DOOR = 0
SWITCH = 1
LAMP = 2
FAN = 3


def isLocked():
    state = customRead(DOOR)
    lock = int(state[2])
    return lock == 1


def isOpen():
    state = customRead(DOOR)
    open = int(state[0])
    return open == 1


def flipFan():
    state = int(customRead(FAN))
    if state == 1:
        customWrite(FAN, 0)
    else:
        customWrite(FAN, 1)


def flipLamp():
    state = int(customRead(LAMP))
    if state == 1:
        customWrite(LAMP, 0)
    else:
        customWrite(LAMP, 1)


def isOn():
    THRESHOLD = 100
    sw = int(digitalRead(SWITCH))
    return sw > THRESHOLD


def lockDoor():
    customWrite(DOOR, "0,1")


def unlockDoor():
    customWrite(DOOR, "0,0")


def main():
    while True:
        while isOn():
            lockDoor()
        else:
            unlockDoor()
        if isLocked():
            continue
        if not isOpen():
            continue
        while isOpen() and not isOn():
            if isOn():
                break
            continue
        else:
            flipFan()
            flipLamp()


if __name__ == "__main__":
    main()
