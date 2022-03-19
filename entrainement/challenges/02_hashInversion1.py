from pwn import *
from helper import readLine
from parse import parse


arrayWords = []
with open("entrainement/docs/words_alpha.txt") as file:
    for line in file:
        arrayWords.append(line.strip("\n"))


r = remote("35.195.130.106", 17005)


readLine(r)

while True:
    line = readLine(r).decode().strip()
    if "Well done" in line or "Wrong" in line:
        break

    parsed = parse("What message hashes to {}?", line)
    if not parsed:
        raise Exception

    hash = parsed[0]

    for word in arrayWords:
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            test = f"{word}{number}"
            result = hashlib.sha1(test.encode()).hexdigest()
            if result == hash:
                r.send(f"{test}\r\n")

readLine(r)
