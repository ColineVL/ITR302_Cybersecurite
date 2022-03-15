from pwn import *

r = remote("35.195.130.106", 17100)

reply = r.recvall()
print(f"Server reply: {reply.decode().strip()}")
r.close()
