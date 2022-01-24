# Libraries
import hashlib
from parse import parse
import base64


def findAPassword(goal):

    # Try to find a password arriving to this hash
    myFile = open("./useful/best110.txt", "r")
    array = myFile.readlines()
    myFile.close()

    arrayStripped = [word.strip("\n") for word in array]

    for word in arrayStripped:
        salt, hashedGoal = goal
        test = f"{salt}{word}"
        # Ils commencent tous par $6$ donc on utilise SHA-512
        hashed = hashlib.sha512(test.encode()).hexdigest()
        print(hashed)
        print(hashedGoal)
        test = base64.b64decode(hashedGoal).hex()
        # Problème base 64 -> hex !!!
        print(test)
        if hashed == hashedGoal:
            return word
    return "found no password"


def getArrayHashes():
    myFile = open("./challenges/HashApplications/leaked_shadow", "r")
    rawArray = myFile.readlines()
    myFile.close()

    arrayHashes = []

    # cf https://linuxize.com/post/etc-shadow-file/

    for line in rawArray:
        # On enlève les infos style username, expiration date...
        encryptedPassword = line.split(":")[1]
        # On découpe les 3 infos
        type, salt, hashed = parse("${}${}${}", encryptedPassword)
        if not type:
            raise Exception("Problem with parsing")

        if type != "6":
            raise Exception("They do not all have type 6")

        arrayHashes.append((salt, hashed))

    print(arrayHashes)
    return arrayHashes


def main():
    arrayHashes = getArrayHashes()

    for goal in arrayHashes:
        word = findAPassword(goal)
        print(word)


main()
