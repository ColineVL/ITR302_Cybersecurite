import hashlib
import string

symbols = string.punctuation

# Je récupère plein de mots depuis le fichier words_alpha.txt
myfile = open("./useful/words_alpha.txt", "r")
arrayWords = myfile.readlines()
myfile.close()
# On enlève les \n
arrayWordsClean = [word.strip("\n") for word in arrayWords]


def findPassword(hash):
    salt = "lrnsodmcbnriwjccbskgfsgrsjclenov"
    for word in arrayWordsClean:
        for symbol in symbols:
            test = f"{word}{symbol}"
            testWithSalt = f"{salt}{test}"
            # Compute hash
            hashTest = hashlib.sha1(testWithSalt.encode()).hexdigest()
            # Check if we found a collision
            if hash == hashTest:
                # print(f"Found {test}")
                return test
    raise Exception("Pas trouvé de password avec ce hash")
