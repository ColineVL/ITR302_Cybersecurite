from pwn import *
import parse

rem = remote("1.1.1.1", 80)
# Get the full reply
rem.send("GET /\r\n\r\n")
reply = rem.recvall()
print(f"Full reply: {reply}")
reply_as_a_string = reply.strip().decode()
# When we perfectly know the reply format we can extract part of the reply easily
parsed = parse.parse("<html>{}</html>", reply_as_a_string)
if not parsed:
    print("The reply is not html code")
else:
    print(f"The code inside the html tags is {parsed[0].strip().encode()}")
rem.close()
