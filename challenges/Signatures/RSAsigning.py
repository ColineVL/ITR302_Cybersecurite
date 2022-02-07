from pwn import *
from parse import parse
from RSA import *

# Connect to remote
# rem = remote("35.195.130.106", 17016)


# def receiveLine():
#     received = rem.readline().strip().decode()
#     print(f"REC {received}")
#     return received


# Receive welcome
# receiveLine()
# receiveLine()

message = "the side must be like a piece of music"
mariaPrivee, mariaPublique = generationClePriveeEtPublique()
raulPrivee, raulPublique = generationClePriveeEtPublique()

# Maria envoie à Raul
ciphertext, signature = envoyerMessageParRSA(message, mariaPublique, mariaPrivee)

# Raul recoit
text = recevoirMessageParRSA(ciphertext, raulPrivee)
print(text)

# Raul vérifie
verifSignature(mariaPublique, signature, text)
