from pwn import *
import parse

rem = remote("1.1.1.1", 80)
# Get the full reply
rem.send("GET /\r\n\r\n")
reply = rem.recvall()
print(f"Full reply: {reply}")
reply_as_a_string = reply.strip().decode()
# We can parse the body without knowing the exact format up to it
parsed = parse.parse("{}<body>{}</body>{}", reply_as_a_string)
if not parsed:
    print("The reply does not have a body")
else:
    print(f"The code inside the body tags is: {parsed[1].strip().encode()}")
    # We have just ignored what was before (parsed[0]) and after (parsed[2]) the body
rem.close()
