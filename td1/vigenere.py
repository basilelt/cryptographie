def vigenere_crypt(message: str, key: str) -> str:
    """Encrypt a message using the Vigenère cipher.

    Each letter is shifted by the corresponding key letter (cycling).
    C_i = (P_i + K_i) mod 26
    """
    key = key.upper()
    result = []
    key_index = 0
    for char in message.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("A")
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


def vigenere_decrypt(message: str, key: str) -> str:
    """Decrypt a Vigenère-encrypted message.

    P_i = (C_i - K_i) mod 26
    """
    key = key.upper()
    result = []
    key_index = 0
    for char in message.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("A")
            result.append(chr((ord(char) - ord("A") - shift) % 26 + ord("A")))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


# ─── Decryption ───────────────────────────────────────────────────────────────

ciphertext = "DIXFSHEWYVZRLKMEIKMBUZDSFSCMCOKSAJSX"
key = "LACRYPTOGRAPHIECESTLAVIE"

plaintext = vigenere_decrypt(ciphertext, key)

print("=== Vigenère Decryption ===")
print(f"  Ciphertext : {ciphertext}")
print(f"  Key        : {key}")
print(f"  Plaintext  : {plaintext}")

# Sanity check: re-encrypting the plaintext should give back the ciphertext
assert vigenere_crypt(plaintext, key) == ciphertext, "Re-encryption mismatch!"
print("  (Re-encryption check passed)")
