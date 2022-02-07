from pwn import *

rem = remote("35.195.130.106", 17100)

# reply = rem.readline()
reply = rem.recvall()
reply_as_a_string = reply.strip().decode()
print(reply_as_a_string)

rem.close()
