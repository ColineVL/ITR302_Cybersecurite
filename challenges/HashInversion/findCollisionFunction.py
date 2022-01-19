import hashlib

N = 48  # 48 premiers bits
n = int(N / 4)

# Je crée un dict : N premiers bits du hash en SHA-256 -> message
myDict = {}


def computeAndPutInDict(message):
    # Je calcule le hash en SHA-256 du message
    hash = hashlib.sha256(message.encode()).hexdigest()
    firstChars = hash[:n]

    # Je regarde si ce hash est dans le dict
    if firstChars in myDict:
        print("YAY! -------------")
        return myDict[firstChars]
    else:
        myDict[firstChars] = message


def findCollision():
    flagFound = False
    msg1 = ""
    msg2 = ""

    # Je récupère plein de mots depuis le fichier words_alpha.txt
    myfile = open("./useful/words_alpha.txt", "r+")
    array = myfile.readlines()
    myfile.close()

    # On enlève les \n
    for i in range(len(array) - 1):
        array[i] = array[i].strip("\n")

    # C'est parti
    for message in array:
        # On ajoute un peu des mots pour avoir un array plus long
        for chiffre in range(50):
            messageDerive = f"{message}{chiffre}{message}"

            if not flagFound:
                result = computeAndPutInDict(messageDerive)
                if result:
                    flagFound = True
                    msg1 = result
                    msg2 = messageDerive

            messageDerive2 = messageDerive.upper()

            if not flagFound:
                result = computeAndPutInDict(messageDerive2)
                if result:
                    flagFound = True
                    msg1 = result
                    msg2 = messageDerive2

    print(f"len du dict : {len(myDict.keys())}")

    if flagFound:
        print("Collision trouvée")
        print(f"Messages : {msg1}, {msg2}")
        hash1 = hashlib.sha256(msg1.encode()).hexdigest()[:n]
        hash2 = hashlib.sha256(msg2.encode()).hexdigest()[:n]
        print(f"Hashes : {hash1}, {hash2}")
        return msg1, msg2

    else:
        print("Aucune collision trouvée")
        return "", ""


# findCollision()

# Nb possibilités pour un hash de 48 bits : 2**48 = 281474976710656
# 2**24 =
# 16777216
# J'en explore
# 37010300

# Collision trouvée
# Messages : cybele11cybele, LAMIIDES44LAMIIDES
# Hashes : 030751c4d66f, 030751c4d66f
