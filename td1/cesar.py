def cesar_crypt(message: str, shift: int = 3) -> str:
    result = []
    for char in message.upper():
        if char.isalpha():
            # Circular shift: map A→0 … Z→25, apply shift, map back
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(char)
    return "".join(result)


def cesar_decrypt(message: str, shift: int = 3) -> str:
    return cesar_crypt(message, -shift)


# ─── 1. Test with VENIVIDIVICI ────────────────────────────────────────────────

plaintext = "VENIVIDIVICI"
ciphertext = cesar_crypt(plaintext)  # default shift of 3
recovered = cesar_decrypt(ciphertext)

print("=== Caesar Cipher (shift = 3) ===")
print(f"  Plaintext  : {plaintext}")
print(f"  Ciphertext : {ciphertext}")  # expected: YHQLYLGLYLFL
print(f"  Decrypted  : {recovered}")
print()


# ─── 2. Automatic cryptanalysis via frequency analysis ─────────────────────

# Relative letter frequencies in French (source: Wikipedia)
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
    """Compute a likelihood score (dot product of letter frequencies)."""
    letters = [c for c in text.upper() if c.isalpha()]
    if not letters:
        return 0.0
    total = len(letters)
    return sum(FREQ_FR.get(c, 0) * (letters.count(c) / total) for c in set(letters))


def cesar_break(ciphertext: str) -> tuple[int, str]:
    """Automatically find the most likely shift."""
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

print("=== Automatic cryptanalysis via frequency analysis ===")
print(f"  Intercepted message: {intercepted}\n")

# Display all candidates with their score
print(f"  {'Shift':>8}  {'Score':>8}  Decrypted text")
print("  " + "-" * 65)
scores = []
for shift in range(26):
    candidate = cesar_decrypt(intercepted, shift)
    s = score(candidate)
    scores.append((s, shift, candidate))
scores.sort(reverse=True)
for s, shift, candidate in scores:
    print(f"  {shift:>8}  {s:>8.4f}  {candidate}")

print()
best_shift, best_text = cesar_break(intercepted)
print(f"  => Shift found automatically: {best_shift}")
print(f"  => Decrypted message: {best_text}")
