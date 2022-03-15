from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
from pwn import *
from parse import parse

from helper import readLine

r = remote("35.195.130.106", 17021)

readLine(r)
readLine(r)

raul_private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048, backend=default_backend()
)
raul_public_key = raul_private_key.public_key()
pem_raul_public_key = raul_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

r.send(f"{pem_raul_public_key.hex()}\r\n")

line = readLine(r).decode().strip()
parsed = parse('{} is: "{}"', line)
if not parsed:
    raise Exception()

encryptedMessage = bytes.fromhex(parsed[1])
readLine(r)

plain_text = raul_private_key.decrypt(
    encryptedMessage,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
# to have a string version
plain_text_string = plain_text.decode()

r.send(f"{plain_text_string}\r\n")
readLine(r)
readLine(r)
