from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature


def generationClePriveeEtPublique():
    # Je génère ma clé privée
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    public_key = private_key.public_key()
    # On encode en octets
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_key, pem_public_key


def envoyerMessageParRSA(message, pem_public_key, ma_cle_privee):
    # J'envoie un message à pem_public_key
    loaded_key_contact = load_pem_public_key(pem_public_key)

    message_bytes = message.encode()

    ciphertext = loaded_key_contact.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    # Signature avec ma clé privée
    signature = ma_cle_privee.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256(),
    )
    return ciphertext, signature


def recevoirMessageParRSA(ciphertext, ma_cle_privee):
    # Je reçois le message
    plain_text = ma_cle_privee.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # to have a string version
    plain_text_string = plain_text.decode()
    return plain_text_string


def verifSignature(cle_publique_envoyeur, signature, plain_text_string):
    plain_text = plain_text_string.encode()
    # Verif de la signature
    loaded_maria_key = load_pem_public_key(cle_publique_envoyeur)
    try:
        verifier = loaded_maria_key.verify(
            signature,
            plain_text,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        print("Signature correct")
        return True
    except InvalidSignature:
        print("Invalid signature")
        return False


def signerAvecPrehashed(prehashed_msg, maClePrivee):
    signature = maClePrivee.sign(
        prehashed_msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        utils.Prehashed(hashes.SHA256()),
    )
    return signature
