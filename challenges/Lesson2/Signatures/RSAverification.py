from pwn import *
from parse import parse
from RSA import *

# Connect to remote
rem = remote("35.195.130.106", 17017)


def receiveLine():
    received = rem.readline().strip().decode()
    print(f"REC {received}")
    return received


# Receive welcome
receiveLine()

# Je reçois la clé publique (PEM convertie en hex)

parsed = parse(
    'Please note my (serialized) RSA public keys (PEM format converted to a hex string): "{}"',
    receiveLine(),
)
if not parsed:
    raise Exception("Problem with parsing")

clePublique = parsed[0]

receiveLine()
receiveLine()

receiveLine()
