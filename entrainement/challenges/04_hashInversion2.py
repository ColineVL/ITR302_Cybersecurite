import hmac

from pwn import *
from helper import readLine
from parse import parse


arrayWords = []
with open("entrainement/docs/words_alpha.txt") as file:
    for line in file:
        arrayWords.append(line.strip("\n"))


r = remote("35.195.130.106", 17007)


readLine(r)

while True:
    line = readLine(r).decode().strip()
    if "Well done" in line or "Wrong" in line:
        break

    parsed = parse("What message hashes to {} with salt {}?", line)
    if not parsed:
        raise Exception

    hash, salt = parsed

    for word in arrayWords:
        for symbol in string.punctuation:
            test = f"{salt}{word}{symbol}"
            result = hashlib.sha1(test.encode()).hexdigest()
            if result == hash:
                r.send(f"{word}{symbol}\r\n")

readLine(r)
readLine(r)
