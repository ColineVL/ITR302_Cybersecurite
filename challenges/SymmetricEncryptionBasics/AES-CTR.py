# Libraries
from pwn import *
from parse import parse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Connect to remote
rem = remote("35.195.130.106", 17011)

# Declarations


def receiveLine():
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()
    print(f"REC {reply_as_a_string}")
    return reply_as_a_string


# Receive welcome
receiveLine()

# Receive key and nonce
keyNonceSentence = receiveLine()
parsed = parse(
    'Bob used AES-CTR with the secret key "{}" and the nonce "{}" to encrypt a plaintext',
    keyNonceSentence,
)
if not parsed:
    print("Problem with first parsing !!!")
else:
    key = bytes.fromhex(parsed[0])
    nonce = bytes.fromhex(parsed[1])

    # Receive message
    messageSentence = receiveLine()
    parsed2 = parse(
        'Please decrypt his message : "{}"',
        messageSentence,
    )
    if not parsed2:
        print("Problem with second parsing !!!")
    else:
        message = bytes.fromhex(parsed2[0])

        # Decrypt and send
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        decryptor = cipher.decryptor()
        decryptedMessage = decryptor.update(message) + decryptor.finalize()
        print(decryptedMessage)
        rem.send(f"{decryptedMessage.decode()}\r\n")

        # Receive answer
        result = receiveLine()

        # Case : problem
        if "Wrong" in result:
            stop = True
            print(f"NOPE {rem.recvall().strip().decode()}")

        # Case : we caught the flag
        elif "Well done" in result:
            print(f"{rem.recvall().strip().decode()}")

rem.close()
