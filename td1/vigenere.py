def vigenere_crypt(message: str, key: str) -> str:
    """
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
    """
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

ciphertext = "DIXFSHEWYVZRLKMEIKMBUZDSFSCMCOKSAJSX"
key = "LACRYPTOGRAPHIECESTLAVIE"

plaintext = vigenere_decrypt(ciphertext, key)

print(f"ciphertext : {ciphertext}")
print(f"key        : {key}")
print(f"plaintext  : {plaintext}")

assert vigenere_crypt(plaintext, key) == ciphertext
