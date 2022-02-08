from pwn import *
from parse import parse
from RSA import *

# Connect to remote
rem = remote("35.195.130.106", 17016)


def receiveLine():
    received = rem.readline().strip().decode()
    print(f"REC {received}")
    return received


# Receive welcome
receiveLine()

# J'envoie ma clé publique
receiveLine()
maPrivee, maPublique = generationClePriveeEtPublique()
rem.send(f"{maPublique.hex()}\r\n")

# J'envoie un message
receiveLine()
message = "Hello World"
ciphertext, signature = envoyerMessageParRSA(message, maPublique, maPrivee)
rem.send(f"{message}\r\n")

# J'envoie la signature
receiveLine()
rem.send(f"{signature.hex()}\r\n")

receiveLine()
receiveLine()
