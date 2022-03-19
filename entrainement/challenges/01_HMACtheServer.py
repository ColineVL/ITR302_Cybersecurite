from hashlib import sha256
import hmac
from pwn import *
from helper import readLine
from parse import parse

r = remote("35.195.130.106", 17004)

username = "gandalfini"
hexKey = "23fb0c2087b7a315603464a695941a37ff7a03066d4f9ecebeda237e8a74be9e"

readLine(r)
readLine(r)
r.send(f"{username}\r\n")
readLine(r)
line = readLine(r).decode().strip()

parsed = parse(
    '{}being "{}" (with {}',
    line,
)
if not parsed:
    raise Exception
message = parsed[1]

tag = hmac.new(bytes.fromhex(hexKey), message.encode(), sha256).hexdigest()

r.send(f"{message}{tag}\r\n")
readLine(r)
readLine(r)
