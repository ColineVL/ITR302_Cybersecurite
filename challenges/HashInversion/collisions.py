# Libraries
from pwn import *

from findCollisionFunction import findCollision

# Connect to remote
rem = remote("35.195.130.106", 17006)

# Declarations
stop = False


def receiveLine():
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()
    print(f"REC {reply_as_a_string}")
    return reply_as_a_string


# Receive welcome
receiveLine()
receiveLine()
msg1, msg2 = findCollision()
receiveLine()
rem.send(f"{msg1}\r\n")
receiveLine()
rem.send(f"{msg2}\r\n")

rem.close()
