from pwn import *
from helper import readLine
from parse import parse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

r = remote("35.195.130.106", 17017)


readLine(r)
line = readLine(r).decode().strip()
parsed = parse('{}: "{}"', line)
if not parsed:
    raise Exception
publicKey = bytes.fromhex(parsed[1])

readLine(r)
readLine(r)

for i in range(30):
    line = readLine(r).decode().strip()
    parsed = parse('{}text "{}" is "{}"', line)
    if not parsed:
        raise Exception
    _, message, sig = parsed

    # vérification
    public_key = load_pem_public_key(publicKey)
    try:
        public_key.verify(
            bytes.fromhex(sig),
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        r.send(f"true\r\n")
    except InvalidSignature:
        r.send(f"false\r\n")


readLine(r)
readLine(r)
