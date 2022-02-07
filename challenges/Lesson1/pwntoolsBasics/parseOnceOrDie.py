from pwn import *
from parse import parse

rem = remote("35.195.130.106", 17102)

# Instructions
for i in range(2):
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()
    print(f"REC {i} {reply_as_a_string}")

stop = False
j = 0

# Receive sentences in latin
while not stop:
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()

    if "Wrong" in reply_as_a_string:
        print(f"NOPE {rem.recvall().strip().decode()}")

    elif "Well done" in reply_as_a_string:
        stop = True
        print(reply_as_a_string)
        print(f"{rem.recvall().strip().decode()}")

    else:
        print(f"REC2 {j} {reply_as_a_string}")
        # Parse and send
        parsed = parse(
            'Please parse this and send me "{}" without the quotes.', reply_as_a_string
        )
        if not parsed:
            print("Problem !!!!!!")
        else:
            print(f"The sentence is : {parsed[0].strip()}")
            rem.send(f"{parsed[0].strip()}\r\n")

    j += 1

rem.close()
