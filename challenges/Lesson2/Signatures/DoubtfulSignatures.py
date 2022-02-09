from pwn import *
from parse import parse
from RSA import *
import hashlib

# Connect to remote
rem = remote("35.195.130.106", 17018)

# Definitions
def receiveLine():
    received = rem.readline().strip().decode()
    print(f"REC {received}")
    return received


# Je récupère des mots
arrayWords = []
with open("./useful/words_alpha.txt") as f:
    arrayWords = f.readlines()
for i in range(len(arrayWords) - 1):
    arrayWords[i] = arrayWords[i].strip("\n")


# Receive welcome
receiveLine()

# Note public key
parsed = parse(
    'Please find my (serialized) RSA public key (in PEM format and converted to a hex string): "{}"',
    receiveLine(),
)
if not parsed:
    raise Exception("Problem with parse")
clePublique = bytes.fromhex(parsed[0])

receiveLine()

# Je recois un texte et une signature
parsed2 = parse('The signature of the text "{}" is "{}"', receiveLine())
if not parsed2:
    raise Exception("Problem with parse2")
text = parsed2[0]
signature = bytes.fromhex(parsed2[1])

receiveLine()

# Je cherche un texte différent avec la même signature
foundWord = "nope"

# Tester pour différents messages
for i, word in enumerate(arrayWords):
    # Je préhashe le mot
    prehashed = ""

    m = hashlib.sha256(word.encode()).digest()
    d = m[0:2].hex() + 60 * "0"
    target_digest = bytes.fromhex(d)

    test = verifSignatureAvecPrehashed(clePublique, signature, target_digest)
    if test:
        foundWord = word
        break
    if i % 5000 == 0:
        print(f"Word {i}/{len(arrayWords)}")
print(f"Mot trouvé : {foundWord}")

# J'ai trouvé un message, je l'envoie
rem.send(f"{foundWord}\r\n")
receiveLine()
receiveLine()
receiveLine()
