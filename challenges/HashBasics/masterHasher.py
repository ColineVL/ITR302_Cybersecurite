# Libraries
from pwn import *
from parse import parse
import hashlib

# Connect to remote
rem = remote("35.195.130.106", 17001)

# Declarations
myDict = {
    "SHA1": hashlib.sha1,
    "SHA224": hashlib.sha224,
    "SHA256": hashlib.sha256,
    "SHA384": hashlib.sha384,
    "SHA512": hashlib.sha512,
    "SHA3-256": hashlib.sha3_256,
    "SHAKE-128": hashlib.shake_128,
}
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
    instruction = receiveLine()

    # Case : problem
    if "Wrong" in instruction:
        stop = True
        print(f"NOPE {rem.recvall().strip().decode()}")

    # Case : we caught the flag
    elif "Well done" in instruction:
        stop = True
        print(f"{rem.recvall().strip().decode()}")

    else:
        # Parse
        print(instruction)
        parsed = parse(
            'Hash me "{}" with {}',
            instruction,
        )
        if not parsed:
            print("Problem with parsing !!!")
        else:
            sentence, algo = parsed
            nbBytes = null

            # Cas particulier : SHAKE-128 with x bytes of output
            if "bytes of output" in algo:
                parsed2 = parse(
                    "{} with {} bytes of output",
                    algo,
                )
                if not parsed:
                    raise Exception("Problem with parsing 2 !!!")
                algo = parsed2[0]
                nbBytes = int(parsed2[1])

                # Hash
                hashFunction = myDict[algo]
                hash = hashFunction(sentence.encode()).hexdigest(nbBytes)
                print(hash)
                rem.send(f"{hash}\r\n")

            # Pas de x bytes of output
            else:
                # Hash
                hashFunction = myDict[algo]
                hash = hashFunction(sentence.encode()).hexdigest()
                print(hash)
                rem.send(f"{hash}\r\n")


rem.close()
