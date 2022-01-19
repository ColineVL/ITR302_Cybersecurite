import hashlib


def findCollision():
    N = 16  # 48 premiers bits
    n = int(N / 4)

    # Je crée un dict : N premiers bits du hash en SHA-256 -> message
    myDict = {}

    flagFound = False
    msg1 = ""
    msg2 = ""

    # Je récupère plein de mots depuis le fichier words_alpha.txt
    myfile = open("./useful/words_alpha.txt", "r")
    array = myfile.readlines()
    myfile.close()

    # On enlève les \n
    for i in range(len(array) - 1):
        array[i] = array[i].strip("\n")

    # On ajoute un peu des mots pour avoir un array plus long
    array2 = []
    for message in array:
        for chiffre in range(50):
            array2.append(f"{message}{chiffre}")
    resultArray = array2 + array

    print(f"len du fichier : {len(array)}")
    print(f"len de ce qu'on ajoute : {len(array2)}")
    print(f"len total : {len(resultArray)}")

    # C'est parti
    for message in resultArray:
        if not flagFound:

            # Je calcule le hash en SHA-256 du message
            hash = hashlib.sha256(message.encode()).hexdigest()
            firstChars = hash[:n]

            # Je regarde si ce hash est dans le dict
            if firstChars in myDict:
                print("YAY! -------------")
                flagFound = True
                msg1 = myDict[firstChars]
                msg2 = message
            else:
                myDict[firstChars] = message

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


findCollision()

# Nb possibilités pour un hash de 48 bits : 281474976710656
# J'en explore 1480412
