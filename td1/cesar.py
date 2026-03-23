def cesar_crypt(message: str, shift: int = 3) -> str:
    result = []
    for char in message.upper():
        if char.isalpha():
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(char)
    return "".join(result)


def cesar_decrypt(message: str, shift: int = 3) -> str:
    return cesar_crypt(message, -shift)


plaintext = "VENIVIDIVICI"
ciphertext = cesar_crypt(plaintext)
recovered = cesar_decrypt(ciphertext)

print(f"plaintext  : {plaintext}")
print(f"ciphertext : {ciphertext}")  # YHQLYLGLYLFL
print(f"decrypted  : {recovered}")
print()


# frequences des lettres en français (Wikipedia)
FREQ_FR = {
    "A": 0.0812,
    "B": 0.0090,
    "C": 0.0334,
    "D": 0.0367,
    "E": 0.1472,
    "F": 0.0109,
    "G": 0.0123,
    "H": 0.0111,
    "I": 0.0723,
    "J": 0.0061,
    "K": 0.0002,
    "L": 0.0534,
    "M": 0.0296,
    "N": 0.0713,
    "O": 0.0524,
    "P": 0.0301,
    "Q": 0.0099,
    "R": 0.0643,
    "S": 0.0887,
    "T": 0.0744,
    "U": 0.0563,
    "V": 0.0183,
    "W": 0.0004,
    "X": 0.0042,
    "Y": 0.0019,
    "Z": 0.0007,
}


def score(text: str) -> float:
    letters = [c for c in text.upper() if c.isalpha()]
    if not letters:
        return 0.0
    total = len(letters)
    return sum(FREQ_FR.get(c, 0) * (letters.count(c) / total) for c in set(letters))


def cesar_break(ciphertext: str) -> tuple[int, str]:
    best_shift, best_text, best_score = 0, ciphertext, -1.0
    for shift in range(26):
        candidate = cesar_decrypt(ciphertext, shift)
        s = score(candidate)
        if s > best_score:
            best_score = s
            best_shift = shift
            best_text = candidate
    return best_shift, best_text


intercepted = "AVJLZJRCREKLIZEXZEMVEKVLIDVTFEELULKVJKUVKLIZEX"

print(f"message intercepté : {intercepted}\n")

scores = []
for shift in range(26):
    candidate = cesar_decrypt(intercepted, shift)
    s = score(candidate)
    scores.append((s, shift, candidate))
scores.sort(reverse=True)

print(f"  {'shift':>6}  {'score':>8}  texte")
print("  " + "-" * 55)
for s, shift, candidate in scores:
    print(f"  {shift:>6}  {s:>8.4f}  {candidate}")

print()
best_shift, best_text = cesar_break(intercepted)
print(f"décalage trouvé : {best_shift}")
print(f"message déchiffré : {best_text}")
