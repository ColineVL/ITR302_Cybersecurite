from pwn import *
import parse
rem = remote("1.1.1.1", 80)
# Get the full reply
rem.send("GET /\r\n\r\n")
reply = rem.recvall()
print(f"Full reply: {reply}")
reply_as_a_string = reply.strip().decode()
# We can parse multiple variables
parsed = parse.parse(b'<html>\r\n<head>{}</head>\r\n<body>\r\n{}</body>\r\n</html>'.decode(), reply_as_a_string)
if not parsed:
  print("The reply is not formated as expected")
else:
  print(f"The code inside the head tags is {parsed[0].strip().encode()}")
  print(f"The code inside the body tags is {parsed[1].strip().encode()}")
rem.close()