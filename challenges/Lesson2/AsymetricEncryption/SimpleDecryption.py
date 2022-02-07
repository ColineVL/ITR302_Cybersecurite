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
    "-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----\n", maPublique.decode()
)
print(maPublique.decode())
truc = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwh26c0yaE5w0c5S71RQ6MlJPWmtxVkQD5WeDe5KD3xYZhSBQbW4Wm3PkVajAQGAFRYKQy8iUHA/qW8PIGVxlN+xgX2sBvOguArDr0RfYigA5cyW+Wo0vM8tfSStkrRYZALQXpXTT24x1cXgXy6vY6aOIWC9xegY6//JaUOdJnXx55mRgdmGLKKGc2ArhkJZNvj4CfpbwXigtzQdo+8D+9qHHEF5nANKlpciIIRfyjiRLCKQF53qLHtYMsaiA0m7wtJP5qSc+CiQyjBkPQbweXMm1OlpdWUPeuyBaIeqrjjJxckEORI9+tbljz0pJ9NUAD/yvPsiBYgrrDVcVPtborQIDAQAB-----END PUBLIC KEY-----"
rem.send(f"{truc}\r\n")


receiveLine()

# # Maria envoie à Raul
# message = "the side must be like a piece of music"
# ciphertext, signature = envoyerMessageParRSA(message, raulPublique, mariaPrivee)

# # Raul recoit
# text = recevoirMessageParRSA(ciphertext, raulPrivee)
# print(text)

# # Raul vérifie
# verifSignature(mariaPublique, signature, text)
