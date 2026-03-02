"""
Vigenere cryptanalysis for Unicode text files encrypted as:

    C_i = P_i + K_(i mod L)

where C_i and P_i are Unicode code points and key bytes K are in [0, 255].
"""

import math
import sys
from collections import Counter
from pathlib import Path

# French character probabilities (rough prior, enough for scoring).
_FREQ_FR = {
    " ": 0.17,
    "\n": 0.01,
    "e": 0.086,
    "a": 0.046,
    "s": 0.080,
    "i": 0.075,
    "t": 0.073,
    "n": 0.071,
    "r": 0.066,
    "u": 0.062,
    "l": 0.054,
    "o": 0.053,
    "d": 0.036,
    "c": 0.033,
    "m": 0.030,
    "p": 0.030,
    "v": 0.018,
    "q": 0.010,
    "f": 0.011,
    "b": 0.009,
    "h": 0.011,
    "g": 0.012,
    "j": 0.006,
    "x": 0.004,
    "y": 0.002,
    "z": 0.001,
    "k": 0.0002,
    "w": 0.0004,
    "é": 0.018,
    "è": 0.006,
    "à": 0.004,
    "ê": 0.003,
    "â": 0.002,
    "î": 0.0012,
    "ï": 0.0008,
    "ô": 0.001,
    "ù": 0.001,
    "û": 0.0005,
    "ç": 0.002,
    "œ": 0.0003,
    ",": 0.010,
    ".": 0.012,
    ";": 0.0015,
    ":": 0.0015,
    "!": 0.0015,
    "?": 0.0015,
    "'": 0.005,
    '"': 0.002,
    "-": 0.003,
    "(": 0.0015,
    ")": 0.0015,
}

for _ch in list(_FREQ_FR):
    if _ch.isalpha() and _ch.lower() == _ch:
        _FREQ_FR[_ch.upper()] = _FREQ_FR[_ch] * 0.20
for _digit in "0123456789":
    _FREQ_FR[_digit] = 0.001

_total = sum(_FREQ_FR.values())
CHAR_LOG_PROB = {ch: math.log(freq / _total) for ch, freq in _FREQ_FR.items()}
LOG_UNK = math.log(1e-8)


def coincidence_rate(data: list[int], lag: int) -> float:
    """P(data[i] == data[i+lag])."""
    n = len(data) - lag
    if n <= 0:
        return 0.0
    matches = sum(1 for i in range(n) if data[i] == data[i + lag])
    return matches / n


def find_key_length(
    data: list[int], max_len: int = 120
) -> tuple[int, dict[int, float]]:
    """
    Detect the period with autocorrelation peaks.
    We keep the smallest lag among those close to the best peak.
    """
    scores = {lag: coincidence_rate(data, lag) for lag in range(1, max_len + 1)}
    best_score = max(scores.values())
    peak_threshold = best_score * 0.95
    near_best = [lag for lag, score in scores.items() if score >= peak_threshold]
    key_length = min(near_best)
    return key_length, scores


def score_shift(counts: Counter[int], shift: int) -> float:
    """Log-likelihood score for one Caesar-like shift on code points."""
    score = 0.0
    for codepoint, count in counts.items():
        plain_code = codepoint - shift
        if plain_code < 0:
            score += count * (LOG_UNK * 4)
            continue
        score += count * CHAR_LOG_PROB.get(chr(plain_code), LOG_UNK)
    return score


def best_shift(subdata: list[int]) -> int:
    """Find the best key byte for one key position."""
    counts = Counter(subdata)
    max_shift = min(255, min(counts))
    best_k = 0
    best_score = float("-inf")
    for k in range(max_shift + 1):
        s = score_shift(counts, k)
        if s > best_score:
            best_score = s
            best_k = k
    return best_k


def find_key(data: list[int], key_length: int) -> bytes:
    return bytes(best_shift(data[i::key_length]) for i in range(key_length))


def decrypt_text(data: list[int], key: bytes) -> str:
    """P_i = C_i - K_(i mod L), without modulo wrapping."""
    klen = len(key)
    out = []
    for i, codepoint in enumerate(data):
        plain_code = codepoint - key[i % klen]
        if plain_code < 0 or plain_code > 0x10FFFF:
            out.append("\ufffd")
        else:
            out.append(chr(plain_code))
    return "".join(out)


def crack_vigenere(filepath: str, max_key_len: int = 120) -> None:
    input_path = Path(filepath)
    cipher_text = input_path.read_text(encoding="utf-8")
    cipher_codes = [ord(ch) for ch in cipher_text]

    print(f"File      : {input_path}")
    print(f"Chars     : {len(cipher_codes)}")
    print()

    # 1. Key length
    print("Searching for key length (autocorrelation peaks)...")
    key_length, scores = find_key_length(cipher_codes, max_key_len)
    print(f"Key length found : {key_length}\n")

    print(f"  {'Lag':>6}  {'Match rate':>10}")
    print("  " + "-" * 23)
    for lag in range(max(1, key_length - 3), min(max_key_len, key_length + 3) + 1):
        marker = "  <===" if lag == key_length else ""
        print(f"  {lag:>6}  {scores[lag]:>10.6f}{marker}")
    print()

    # 2. Key recovery
    key = find_key(cipher_codes, key_length)
    key_latin1 = key.decode("latin-1")
    key_readable = "".join(
        ch if ch.isprintable() and ch not in "\r\n\t" else f"\\x{ord(ch):02x}"
        for ch in key_latin1
    )
    print(f"Key found        : {key_readable}  (hex: {key.hex()})")
    print()

    # 3. Decrypt
    plaintext = decrypt_text(cipher_codes, key)

    # 4. Save and preview
    if input_path.suffix == ".txt":
        out_path = input_path.with_name(f"{input_path.stem}_decrypted.txt")
    else:
        out_path = input_path.with_name(f"{input_path.name}_decrypted.txt")
    out_path.write_text(plaintext, encoding="utf-8")

    print("=== Decrypted (first 500 chars) ===")
    print(plaintext[:500])
    print(f"\nFull output saved to: {out_path}")


if __name__ == "__main__":
    default_path = Path(__file__).with_name("crypted_vigenere.txt")
    filepath = sys.argv[1] if len(sys.argv) > 1 else str(default_path)
    crack_vigenere(filepath)
