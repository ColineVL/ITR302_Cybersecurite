# Libraries
from pwn import *
from parse import parse
import hashlib

# Connect to remote
rem = remote("35.195.130.106", 17003)

# Values
def receiveLine():
    line = rem.readline().strip().decode()
    print(f"REC {line}")
    return line


def randomword():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(10))


def findIndex(message):
    while True:
        index = randomword()
        total = f"{message}{index}"

        # Compute SHA256, hex digest
        hexDigest = hashlib.sha256(total.encode()).hexdigest()

        # Start with 4 zeros ?
        if hexDigest[:4] == "0000":
            return index


def main():
    # Receive instructions
    receiveLine()
    receiveLine()

    # The problem
    line = receiveLine()
    (message,) = parse(
        'Send me an index so that the hex digest SHA256(m||index) starts with 4 zeros with m being "{}" (without the double quotes)',
        line,
    )
    if not message:
        raise Exception("Problem with parse")

    result = findIndex(message)
    rem.send(f"{result}\r\n")
    print(rem.recvall().strip().decode())


main()
