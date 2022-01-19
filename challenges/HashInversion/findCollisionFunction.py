import string
import random
import hashlib


def findCollision():

    # Je crée un dict : 48 premiers bits du hash en SHA-256 -> message
    myDict = {}

    flagFound = False
    msg1 = ""
    msg2 = ""

    while not flagFound:
        # Je crée un message
        length_of_string = 8
        message = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(length_of_string)
        )
        print(message)

        # TODO plutot utiliser words-alpha.txt ???????

        # Je vérifie qu'on n'est pas déjà tombés sur ce message
        if not message in myDict.values():

            # Je calcule le hash en SHA-256 du message
            hash = hashlib.sha256(message.encode()).hexdigest()
            firstChars = hash[:48]

            # Je regarde si ce hash est dans le dict
            if firstChars in myDict:
                print("YAY! -------------")
                flagFound = True
                msg1 = myDict[firstChars]
                msg2 = message
            else:
                myDict[firstChars] = message

    print(f"{msg1}, {msg2}")
    hash1 = hashlib.sha256(msg1.encode()).hexdigest()[:4]
    hash2 = hashlib.sha256(msg2.encode()).hexdigest()[:4]
    print(f"{hash1}, {hash2}")
    return msg1, msg2


findCollision()
