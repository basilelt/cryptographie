#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# 1. Encrypt the poeme.txt file using AES in CBC mode
def encrypt_file_cbc(input_file, output_file):
    # Generate a random 256-bit (32-byte) key
    key = get_random_bytes(32)
    # Generate a random initialization vector (IV) of 16 bytes
    iv = get_random_bytes(16)

    # Create an AES encryption object in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Read the input file
    with open(input_file, "rb") as f:
        plaintext = f.read()

    # Apply padding and encrypt
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # Write the key, IV, and ciphertext to the output file
    with open(output_file, "wb") as f:
        f.write(key)
        f.write(iv)
        f.write(ciphertext)

    print(f"File encrypted successfully: {output_file}")


# 2. Decrypt the file encrypted with AES in CBC mode
def decrypt_file_cbc(input_file, output_file):
    # Read the key, IV, and ciphertext from the input file
    with open(input_file, "rb") as f:
        key = f.read(32)
        iv = f.read(16)
        ciphertext = f.read()

    # Create an AES decryption object in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt and remove padding
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Write the plaintext to the output file
    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"File decrypted successfully: {output_file}")


# 3. Decrypt the secrets.jpg file using AES in CTR mode
def decrypt_file_ctr(input_file, output_file, key, nonce_size=8):
    # Read the nonce and ciphertext from the input file
    with open(input_file, "rb") as f:
        nonce = f.read(nonce_size)
        ciphertext = f.read()

    # Create an AES decryption object in CTR mode
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)

    # Decrypt
    plaintext = cipher.decrypt(ciphertext)

    # Write the plaintext to the output file
    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"File decrypted successfully: {output_file}")


if __name__ == "__main__":
    # Encrypt the poeme.txt file
    encrypt_file_cbc("poeme.txt", "poeme_encrypted.txt")

    # Decrypt the poeme_encrypted.txt file
    decrypt_file_cbc("poeme_encrypted.txt", "poeme_decrypted.txt")

    # Decrypt the secrets.jpg file
    key = b"\x97N2\xcb\xf615i\x1b\xb6qs\xf6\xe2\x9d\xdb"
    decrypt_file_ctr("secrets.jpg", "secrets_decrypted.jpg", key)
