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

r = remote("35.195.130.106", 17016)


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
readLine(r)
message = "Hello"
r.send(f"{message}\r\n")


readLine(r)

signature = raul_private_key.sign(
    message.encode(),
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256(),
)

r.send(f"{signature.hex()}\r\n")
readLine(r)
readLine(r)
