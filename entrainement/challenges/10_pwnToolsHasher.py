import hashlib
from pwn import *
from helper import readLine
from parse import parse

r = remote("35.195.130.106", 17002)

readLine(r)

while True:
    line = readLine(r).decode().strip()
    if "Well done" in line or "Wrong" in line:
        break

    parsed = parse('Hash me "{}" with {}', line)
    if not parsed:
        raise Exception
    latin, algo = parsed
    my_dict = {
        "SHA1": hashlib.sha1,
        "SHA256": hashlib.sha256,
        "MD5": hashlib.md5,
        "SHA3-256": hashlib.sha3_256,
        "SHAKE-128 with 1024 bytes of output": hashlib.shake_128,
    }

    fonction = my_dict[algo]
    m = fonction()
    m.update(latin.encode())
    result = (
        m.hexdigest()
        if algo != "SHAKE-128 with 1024 bytes of output"
        else m.hexdigest(1024)
    )

    r.send(f"{result}\r\n")

readLine(r)
