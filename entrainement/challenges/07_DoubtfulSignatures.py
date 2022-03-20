from parse import parse
from helper import readLine
from pwn import *

from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature


arrayWords = []
with open("entrainement/docs/words_alpha.txt") as file:
    for word in file:
        arrayWords.append(word.strip("\n"))

r = remote("35.195.130.106", 17018)

readLine(r)
line = readLine(r).decode().strip()
parsed = parse('{}: "{}"', line)
if not parsed:
    raise Exception
publicKey = bytes.fromhex(parsed[1])
public_key = load_pem_public_key(publicKey)

readLine(r)


line = readLine(r).decode().strip()
parsed = parse('{}text "{}" is "{}"', line)
if not parsed:
    raise Exception
_, latin, sig = parsed
signature = bytes.fromhex(sig)

readLine(r)

# trouver un message avec la même signature
def trouveMemeSignature():
    for message in arrayWords:

        try:

            hasher = hashes.Hash(hashes.SHA256())
            hasher.update(message.encode())
            digest = hasher.finalize()
            d = digest[0:2].hex() + 60 * "0"
            target_digest = bytes.fromhex(d)

            public_key.verify(
                signature,
                target_digest,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                utils.Prehashed(hashes.SHA256()),
            )
            return message
        except InvalidSignature:
            a = 0
    return "nope"


message = trouveMemeSignature()
print(message)
r.send(f"{message}\r\n")
readLine(r)
readLine(r)
readLine(r)
