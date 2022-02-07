from pwn import *
from parse import parse

rem = remote("35.195.130.106", 17103)

# Declarations
myDict = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5}
stop = False
j = 0

# Instructions
for i in range(2):
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()
    print(f"REC {i} {reply_as_a_string}")

# Receive sentences in latin
while not stop:
    reply = rem.readline()
    reply_as_a_string = reply.strip().decode()

    # Case : problem
    if "Wrong" in reply_as_a_string:
        stop = True
        print(f"NOPE {rem.recvall().strip().decode()}")

    # Case : we caught the flag
    elif "Well done" in reply_as_a_string:
        stop = True
        print(reply_as_a_string)
        print(f"{rem.recvall().strip().decode()}")

    else:
        print(f"REC2 {j} {reply_as_a_string}")
        # Parse and send
        parsed = parse(
            'Please parse this and send me the {} word of "{}" without the quotes.',
            reply_as_a_string,
        )
        if not parsed:
            print("Problem !!!!!!")
        else:
            sentence = parsed[1]
            n = parsed[0]
            # We want to get the n-th word of sentence
            sentenceArray = sentence.split(" ")
            number = myDict[n]
            result = sentenceArray[number - 1]
            rem.send(f"{result}\r\n")

    j += 1

rem.close()
