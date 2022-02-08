from pwn import *
from parse import parse
from RSA import *

# Connect to remote
rem = remote("35.195.130.106", 17021)


def receiveLine():
    received = rem.readline().strip().decode()
    print(f"REC {received}")
    return received


# Receive welcome
receiveLine()
receiveLine()

# Je send ma clé publique
maPrivee, maPublique = generationClePriveeEtPublique()
rem.send(f"{maPublique.hex()}\r\n")


receiveLine()

# Récupérer ciphertext
# parsed = parse("{}", receiveLine())
# if not parsed:
#     raise Exception("problem with parse")
# ciphertext = parsed[0]

# # Je décrypte le texte
# text = recevoirMessageParRSA(ciphertext, maPrivee)
# print(text)

# rem.send(f"{text}\r\n")

# receiveLine()
# receiveLine()
