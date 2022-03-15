from pwn import *

from helper import readLine

r = remote("35.195.130.106", 17101)

readLine(r)
readLine(r)

stop = False
while not stop:
    line = readLine(r).decode().strip()
    if "Well" in line:
        stop = True
        readLine(r)
    else:
        r.send(f"{line}\r\n")


r.close()
