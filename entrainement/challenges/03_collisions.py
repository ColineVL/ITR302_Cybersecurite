from pwn import *
from helper import readLine


def findCollision():
    my_dict = {}
    for word in arrayWords[:167702]:
        for number in range(50):
            test = f"{word}{number}{word}"
            result = hashlib.sha256(test.encode()).hexdigest()
            result = result[:12]
            if result in my_dict:
                print(f"trouvé ! {test}")
                msg1 = my_dict[result]
                msg2 = test
                return msg1, msg2
            my_dict[result] = test

            test2 = test.upper()
            result2 = hashlib.sha256(test2.encode()).hexdigest()
            result2 = result2[:12]
            if result2 in my_dict:
                print(f"trouvé ! - {test}")
                msg1 = my_dict[result2]
                msg2 = test2
                return msg1, msg2
            my_dict[result2] = test2

    return "nope", "nope"


arrayWords = []
with open("entrainement/docs/words_alpha.txt") as file:
    for line in file:
        arrayWords.append(line.strip("\n"))


r = remote("35.195.130.106", 17006)


readLine(r)
readLine(r)
print("Starting")

msg1, msg2 = findCollision()
print(msg1, msg2)
if msg1 != msg2:
    readLine(r)
    r.send(f"{msg1}\r\n")
    readLine(r)
    r.send(f"{msg2}\r\n")

    readLine(r)
    readLine(r)
