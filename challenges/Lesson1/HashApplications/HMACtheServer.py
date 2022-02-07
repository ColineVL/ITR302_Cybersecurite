# Libraries
from pwn import *
from parse import parse
import hmac

# Connect to remote
rem = remote("35.195.130.106", 17004)

# Values
def receiveLine():
    line = rem.readline().strip().decode()
    print(f"REC {line}")
    return line


login = "gandalfini"
keyHex = "23fb0c2087b7a315603464a695941a37ff7a03066d4f9ecebeda237e8a74be9e"
keyBytes = bytes.fromhex(keyHex)

# Receive instructions
receiveLine()
receiveLine()
rem.send(f"{login}\r\n")
receiveLine()

# Authenticated message
line = receiveLine()
(message,) = parse(
    'Now send me an authenticated message m||t with t an HMAC-SHA256 tag generated with our common secret, and m being "{}" (with the final space but without the double quotes):',
    line,
)
if not message:
    raise Exception("Problem with parsing")

resultMac = hmac.digest(keyBytes, message.encode(), "sha256").hex()
rem.send(f"{message}{resultMac}\r\n")

print(rem.recvall().strip().decode())
