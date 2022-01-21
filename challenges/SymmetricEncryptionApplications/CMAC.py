# Libraries
from typing import Text
from pwn import *
from parse import parse
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms

# Connect to remote
rem = remote("35.195.130.106", 17015)

# Declarations
def receiveLine():
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()
    print(f"REC {reply_as_a_string}")
    return reply_as_a_string


# Receive welcome
receiveLine()

# Receive key
keySentence = receiveLine()
(key,) = parse(
    'I remind you that we have previously shared the key : "{}"', keySentence
)
if not key:
    raise Exception("Problem with parsing the key")
print(key)
key = bytes.fromhex(key)

# Receive text
sentence = receiveLine()
(text,) = parse(
    'Could you please send me the CMAC of the text : "{}" generated with our common key?',
    sentence,
)
if not text:
    raise Exception("Problem with parsing the text")
text = text.encode()

# Compute the CMAC of the text
c = cmac.CMAC(algorithms.AES(key))
c.update(text)
CMACcomputed = c.finalize().hex()

rem.send(f"{CMACcomputed}\r\n")

# Receive answer
print(f"{rem.recvall().strip().decode()}")

rem.close()
