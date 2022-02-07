from pwn import *
from parse import parse
from RSA import *
import base64

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
parsed = parse(
    "-----BEGIN PUBLIC KEY-----\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n-----END PUBLIC KEY-----\n",
    maPublique.decode(),
)
if not parsed:
    raise Exception("Problem with parse")

keyEncoded = "".join(parsed).encode().hex()
rem.send(f"{keyEncoded}\r\n")

# J'envoie un message
receiveLine()
message = "Hello World"
ciphertext, signature = envoyerMessageParRSA(message, maPublique, maPrivee)
rem.send(f"{ciphertext}\r\n")

# J'envoie la signature
receiveLine()
signatureEncoded = base64.urlsafe_b64encode(signature).hex()
rem.send(f"{signatureEncoded}\r\n")

receiveLine()
