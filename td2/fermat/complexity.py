"""
Étude expérimentale de la complexité du test de primalité de Fermat.

Complexité attendue : O(b³) en nombre de bits b = ⌊log₂(n)⌋
  - pow(a, n-1, n) effectue O(b) multiplications modulaires
  - chaque multiplication de b bits coûte O(b²) (Python: Karatsuba/GMP)
  → temps polynomial en b  (≠ exponentiel pour le test naïf)
"""

import time
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from main import is_prime_fermat
from sympy import nextprime


def measure(n: int, repeats: int = 50) -> float:
    """Temps moyen (s) pour appeler is_prime_fermat(n)."""
    t0 = time.perf_counter()
    for _ in range(repeats):
        is_prime_fermat(n)
    return (time.perf_counter() - t0) / repeats


def run():
    # Premiers proches de 2^b pour b allant de 10 à 2000
    # → range bien plus large que le test naïf (polynomial, pas exponentiel)
    bits_targets = list(range(10, 2001, 50))
    candidates = [int(nextprime(1 << b)) for b in bits_targets]
    times = [measure(n) for n in candidates]

    bits = [n.bit_length() for n in candidates]

    # --- Tableau (condensé) ---
    print(f"{'b':>5}  {'temps (µs)':>12}")
    print("-" * 20)
    for b, t in zip(bits, times):
        print(f"{b:>5}  {t*1e6:>12.4f}")

    # --- Régressions ---
    log_b = np.log(bits)
    log_t = np.log(times)
    slope_b, intercept_b = np.polyfit(log_b, log_t, 1)
    print(f"\nPente log-log (vs b) = {slope_b:.3f}  (attendu ≈ 3.0 pour O(b³))")

    # Semi-log vs b : doit être courbé (exponentiel serait une droite)
    slope_semi, intercept_semi = np.polyfit(bits, log_t, 1)

    # --- Graphiques ---
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Temps vs b (linéaire)
    ax1.plot(bits, [t * 1e6 for t in times], "o-", linewidth=1.5, markersize=4)
    ax1.set_xlabel("b = ⌊log₂(n)⌋  (nombre de bits)")
    ax1.set_ylabel("Temps moyen (µs)")
    ax1.set_title("Temps vs b  —  croissance polynomiale")
    ax1.grid(True)

    # 2. log(temps) vs log(b) : droite de pente ≈ 3
    ax2.plot(log_b, log_t, "o", markersize=4, label="mesures")
    ax2.plot(log_b, slope_b * log_b + intercept_b, "--",
             label=f"régression : pente = {slope_b:.2f}\n(attendu ≈ 3.0)")
    ax2.set_xlabel("log(b)")
    ax2.set_ylabel("log(temps)")
    ax2.set_title("log-log → pente ≈ 3 confirme O(b³)")
    ax2.legend()
    ax2.grid(True)

    # 3. Semi-log vs b : courbé (≠ test naïf qui est une droite)
    b_arr = np.array([min(bits), max(bits)])
    ax3.semilogy(bits, [t * 1e6 for t in times], "o-", linewidth=1.5, markersize=4,
                 label="mesures")
    ax3.semilogy(b_arr, np.exp(slope_semi * b_arr + intercept_semi) * 1e6, "--",
                 color="gray", label="fit linéaire (si exponentiel → droite)")
    ax3.set_xlabel("b = ⌊log₂(n)⌋")
    ax3.set_ylabel("Temps moyen (µs)  [échelle log]")
    ax3.set_title("Semi-log vs b — courbé ≠ naïf (droite)")
    ax3.legend()
    ax3.grid(True, which="both")

    plt.suptitle("Test de Fermat — complexité O(b³) polynomiale en b", fontsize=13)
    plt.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "complexity_fermat.png")
    plt.savefig(out, dpi=150)
    print(f"Graphique sauvegardé : {out}")
    plt.show()


if __name__ == "__main__":
    run()
