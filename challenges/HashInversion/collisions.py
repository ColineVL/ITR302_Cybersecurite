# Libraries
from pwn import *

# from findCollisionFunction import findCollision

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

# msg1, msg2 = findCollision()
# Collision trouvée
# Messages : cybele11cybele, LAMIIDES44LAMIIDES
# Hashes : 030751c4d66f, 030751c4d66f

msg1 = "cybele11cybele"
msg2 = "LAMIIDES44LAMIIDES"

if msg1 != "":
    receiveLine()
    rem.send(f"{msg1}\r\n")
    receiveLine()
    rem.send(f"{msg2}\r\n")
    print(f"{rem.recvall().strip().decode()}")

rem.close()
