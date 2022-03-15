import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from pwn import *
from parse import parse

from helper import readLine

r = remote("35.195.130.106", 17011)

readLine(r)
line = readLine(r).decode().strip()
parsed = parse(
    'Bob used AES-CTR with the secret key "{}" and the nonce "{}" to encrypt a plaintext',
    line,
)
if not parsed:
    raise Exception()
key, nonce = parsed
key = bytes.fromhex(key)
nonce = bytes.fromhex(nonce)
line = readLine(r).decode().strip()
parsed = parse('Please decrypt his message : "{}"', line)
if not parsed:
    raise Exception()
message = parsed[0]
message = bytes.fromhex(message)


cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
decryptor = cipher.decryptor()
trad = decryptor.update(message) + decryptor.finalize()
trad = trad.decode()
r.send(f"{trad}\r\n")
readLine(r)
readLine(r)
