from pwn import *
from parse import parse

from helper import readLine

r = remote("35.195.130.106", 17102)

readLine(r)
readLine(r)

stop = False
while not stop:
    line = readLine(r).decode().strip()
    if "Well" in line:
        stop = True
        readLine(r)
    else:
        parsed = parse('Please parse this and send me "{}" without the quotes.', line)
        if not parsed:
            raise Exception()
        latin = parsed[0]
        r.send(f"{latin}\r\n")


r.close()
