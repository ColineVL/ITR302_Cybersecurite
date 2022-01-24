# Libraries
from parse import parse
import crypt


def getCommonPasswords():
    myFile = open("./useful/best110.txt", "r")
    array = myFile.readlines()
    myFile.close()

    return [word.strip("\n") for word in array]


def findAPassword(goal):
    # On extrait le salt et le type
    type, salt, _ = parse("${}${}${}", goal)
    if not type:
        raise Exception("Problem with parsing")

    # Try to find a password arriving to this hash
    arrayStripped = getCommonPasswords()

    for word in arrayStripped:
        test = crypt.crypt(word, f"${type}${salt}")
        if test == goal:
            return word

    return "found no password"


def getArrayHashes():
    myFile = open("./challenges/HashApplications/leaked_shadow", "r")
    rawArray = myFile.readlines()
    myFile.close()

    # cf https://linuxize.com/post/etc-shadow-file/
    # On enlève les infos style username, expiration date...
    return [line.split(":")[1] for line in rawArray]


def main():
    arrayHashes = getArrayHashes()
    result = [findAPassword(goal) for goal in arrayHashes]
    # On retravaille le résultat pour obtenir une ligne :
    # Please submit the passwords of the users following the order of the file separated by semicolons (no spaces).
    print(";".join(result))


main()
