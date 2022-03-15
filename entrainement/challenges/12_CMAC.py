from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from pwn import *
from parse import parse

from helper import readLine

r = remote("35.195.130.106", 17015)

readLine(r)

line = readLine(r).decode().strip()
parsed = parse(
    'I remind you that we have previously shared the key : "{}"',
    line,
)
if not parsed:
    raise Exception()
key = bytes.fromhex(parsed[0])
line = readLine(r).decode().strip()
parsed = parse(
    'Could you please send me the CMAC of the text : "{}" generated with our common key?',
    line,
)
if not parsed:
    raise Exception()
message = parsed[0]


c = cmac.CMAC(algorithms.AES(key))
c.update(message.encode())
cmacComputed = c.finalize()

r.send(f"{cmacComputed.hex()}\r\n")

readLine(r)
readLine(r)
