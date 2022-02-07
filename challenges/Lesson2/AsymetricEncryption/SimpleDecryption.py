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
parsed = parse(
    "-----BEGIN PUBLIC KEY-----\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n-----END PUBLIC KEY-----\n",
    maPublique.decode(),
)
if not parsed:
    raise Exception("Problem with parse")

keyEncoded = "".join(parsed).encode().hex()
rem.send(f"{keyEncoded}\r\n")


receiveLine()

# # Maria envoie à Raul
# message = "the side must be like a piece of music"
# ciphertext, signature = envoyerMessageParRSA(message, raulPublique, mariaPrivee)

# # Raul recoit
# text = recevoirMessageParRSA(ciphertext, raulPrivee)
# print(text)

# # Raul vérifie
# verifSignature(mariaPublique, signature, text)
