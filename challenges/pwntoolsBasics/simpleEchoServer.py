from pwn import *

rem = remote("35.195.130.106", 17101)

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
        rem.send(reply_as_a_string + "\r\n")

    j += 1
