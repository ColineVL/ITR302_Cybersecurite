from pwn import *
from parse import parse

from helper import readLine

r = remote("35.195.130.106", 17103)

readLine(r)
readLine(r)

stop = False
while not stop:
    line = readLine(r).decode().strip()
    if "Well" in line:
        stop = True
        readLine(r)
    else:
        parsed = parse(
            'Please parse this and send me the {} word of "{}" without the quotes.',
            line,
        )
        if not parsed:
            raise Exception("Problem with parse")
        number, latin = parsed
        my_dict = {"first": 0, "second": 1, "third": 2, "fourth": 3, "fifth": 4}
        arrayLatin = latin.split(" ")

        r.send(f"{arrayLatin[my_dict[number]]}\r\n")


r.close()
