# Libraries
from pwn import *
from parse import parse

from findPasswordFunction import findPassword

# Connect to remote
rem = remote("35.195.130.106", 17007)

# Declarations
stop = False


def receiveLine(i):
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()
    print(f"REC {i} {reply_as_a_string}")
    return reply_as_a_string


# Receive welcome
receiveLine(0)
# receiveLine()

i = 0
# Receive instructions
while not stop:
    line = receiveLine(i)
    i += 1

    if "message" in line:
        # Parse
        hash, salt = parse("What message hashes to {} with salt {}?", line)
        if not hash:
            raise Exception("Problem with parse")

        # The attacker uses a word and a symbol, and a salt
        # Let's do a brute force attack using a dictionnaire
        rep = findPassword(hash)
        rem.send(f"{rep}\r\n")

    else:
        stop = True
        print(f"{rem.recvall().strip().decode()}")

rem.close()
