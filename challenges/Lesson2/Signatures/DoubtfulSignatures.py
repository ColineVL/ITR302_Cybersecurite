from pwn import *
from parse import parse
from RSA import *
import hashlib

# Connect to remote
rem = remote("35.195.130.106", 17018)


def receiveLine():
    received = rem.readline().strip().decode()
    print(f"REC {received}")
    return received


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
foundWord = ""

# Je récupère des mots
arrayWords = []
with open("./useful/words_alpha.txt") as f:
    arrayWords = f.readlines()
for i in range(len(arrayWords) - 1):
    arrayWords[i] = arrayWords[i].strip("\n")


# word = "aah"
# test = verifSignature(clePublique, signature, word)
# if test:
#     print("yes")
# else:
#     print("no")

# # Tester pour différents messages
# for word in arrayWords:
#     print(word.encode())
#     prehashed_msg = hashlib.sha256(word.encode()).digest()
#     d = prehashed_msg[0:2].hex() + 60 * "0"
#     target_digest = bytes.fromhex(d)
#     signatureTest = signerAvecPrehashed(target_digest, maPrivee).hex()
#     assert len(signatureHex) == len(signatureTest)
#     if signatureTest == signatureHex:
#         foundWord = word
#         print("TROUVEEEEEEEE")

# # print(foundWord)
