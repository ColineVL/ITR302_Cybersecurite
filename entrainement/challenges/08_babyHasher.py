import hashlib
from pwn import *
from helper import readLine
from parse import parse

r = remote("35.195.130.106", 17000)

readLine(r)
line = readLine(r).decode().strip()
parsed = parse('Hash me "{}" with SHA256', line)
if not parsed:
    raise Exception
latin = parsed[0]

m = hashlib.sha256()
m.update(latin.encode())
result = m.hexdigest()

r.send(f"{result}\r\n")
readLine(r)
readLine(r)
