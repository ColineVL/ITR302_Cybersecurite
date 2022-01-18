from pwn import *

rem = remote("35.195.130.106", 17101)

reply_as_a_string = rem.recvall().strip().decode()
print(reply_as_a_string)
rem.send("GET /\r\n\r\n")
reply = rem.readline()
print(reply)
