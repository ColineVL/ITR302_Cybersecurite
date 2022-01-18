from pwn import *

r = remote("google.com", 443, ssl=True)
# HTML hint for next line.
# The \r\n\r\n is just what HTML requires to understand that you have ended your
# command and not doing a newline. So basically you ask "GET /" and say "over".
r.send("GET /\r\n\r\n")
reply = r.readline()
print(f"Server reply: {reply}")
print(f"Server reply as a string: {reply.decode()}")
r.close()
