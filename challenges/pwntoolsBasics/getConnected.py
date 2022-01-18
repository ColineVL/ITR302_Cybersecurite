from pwn import *

rem = remote("35.195.130.106", 17100)

reply_as_a_string = rem.recvall().strip().decode()
print(reply_as_a_string)

rem.close()
