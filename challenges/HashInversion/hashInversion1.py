# Libraries
from pwn import *
from parse import parse

# Connect to remote
rem = remote("35.195.130.106", 17005)

# Declarations
stop = False


def receiveLine():
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()
    print(f"REC {reply_as_a_string}")
    return reply_as_a_string


# Receive welcome
receiveLine()

# Receive instructions
while not stop:
    line = receiveLine()

    # Case : problem
    if "Nope" in line:
        stop = True
        print(f"NOPE {rem.recvall().strip().decode()}")

    # Case : we caught the flag
    elif "Well done" in line:
        stop = True
        print(f"{rem.recvall().strip().decode()}")

    else:
        # Parse

        parsed = parse("What message hashes to {}?", line)
        if not parsed:
            raise Exception("Problem with parse")
        else:
            hash = parsed[0]
            rep = ""

        # NB : we use https://hashes.com/en/decrypt/hash
        if hash == "1526f60c6e677d88ed77cd19075e1b8434cac2b4":
            rep = "love7"
        if hash == "da743904482e1958e440cb1197191615d80b0ed7":
            rep = "life0"
        if hash == "ac1634a13c4c923b50e10694cc1d3aae2686193f":
            rep = "rock4"

        print(rep)
        rem.send(f"{rep}\r\n")

rem.close()
