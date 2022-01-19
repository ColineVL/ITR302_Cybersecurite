# Libraries
from pwn import *
from parse import parse
import hashlib

# Connect to remote
rem = remote("35.195.130.106", 17000)

# Declarations
def receiveLine():
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()
    print(f"REC {reply_as_a_string}")
    return reply_as_a_string


# Receive welcome
receiveLine()

# Receive sentence
fullSentence = receiveLine()
parsed = parse(
    'Hash me "{}" with SHA256',
    fullSentence,
)
if not parsed:
    print("Problem with first parsing !!!")
else:
    sentence = parsed[0]
    print(sentence)

    # Hash
    hash = hashlib.sha256(sentence.encode()).hexdigest()
    print(hash)
    rem.send(f"{hash}\r\n")

    # Receive answer
    print(f"{rem.recvall().strip().decode()}")


rem.close()
