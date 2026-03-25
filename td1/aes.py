#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def encrypt_file_cbc(input_file, output_file):
    key = get_random_bytes(32)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(input_file, "rb") as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # format: key (32) | iv (16) | ciphertext
    with open(output_file, "wb") as f:
        f.write(key)
        f.write(iv)
        f.write(ciphertext)

    print(f"encrypted: {output_file}")


def decrypt_file_cbc(input_file, output_file):
    with open(input_file, "rb") as f:
        key = f.read(32)
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"decrypted: {output_file}")


def decrypt_file_ctr(input_file, output_file, key, nonce_size=8):
    with open(input_file, "rb") as f:
        nonce = f.read(nonce_size)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"decrypted: {output_file}")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Encrypt the poeme.txt file
    encrypt_file_cbc("poeme.txt", "poeme_encrypted.txt")

    # Decrypt the poeme_encrypted.txt file
    decrypt_file_cbc("poeme_encrypted.txt", "poeme_decrypted.txt")

    # Decrypt the secrets.jpg file
    key = b"\x97N2\xcb\xf615i\x1b\xb6qs\xf6\xe2\x9d\xdb"
    decrypt_file_ctr("secrets.jpg", "secrets_decrypted.jpg", key)
