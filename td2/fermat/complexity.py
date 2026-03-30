"""
Étude expérimentale de la complexité du test de primalité naïf.
"""

import math
import time
import numpy as np
import matplotlib.pyplot as plt

from main import is_prime_fermat


def next_prime(start: int) -> int:
    """Retourne le plus petit premier >= start."""
    n = start | 1  # force impair
    while not is_prime_fermat(n):
        n += 2
    return n


def measure(n: int, repeats: int = 30) -> float:
    """Temps moyen (s) pour tester la primalité de n."""
    t0 = time.perf_counter()
    for _ in range(repeats):
        is_prime_fermat(n)
    return (time.perf_counter() - t0) / repeats


def run():
    # Pire cas : n premier → on parcourt tous les diviseurs jusqu'à √n
    # Valeurs logarithmiquement espacées entre 10^1 et 10^8
    ns_raw = np.logspace(1, 8, num=40, dtype=int)
    candidates = [next_prime(int(n)) for n in ns_raw]
    times = [measure(n) for n in candidates]
    sqrts = [math.sqrt(n) for n in candidates]

    bits = [n.bit_length() for n in candidates]

    # --- Tableau ---
    print(f"{'b':>4}  {'n':>12}  {'√n':>10}  {'temps (µs)':>12}")
    print("-" * 43)
    for b, n, sq, t in zip(bits, candidates, sqrts, times):
        print(f"{b:>4}  {n:>12}  {sq:>10.1f}  {t*1e6:>12.4f}")

    # --- Régressions ---
    log_n = np.log(candidates)
    log_t = np.log(times)
    slope, intercept = np.polyfit(log_n, log_t, 1)
    print(f"\nPente log-log (vs n) = {slope:.3f}  (attendu ≈  O(log2(n^3)))")

    # Régression linéaire temps ~ A * 2^(b/2) → log(temps) linéaire en b
    slope_b, intercept_b = np.polyfit(bits, log_t, 1)
    print(f"Pente log(temps) vs b = {slope_b:.4f}  (attendu ≈ )")

    # --- Graphiques ---
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    ax1.plot(candidates, [t * 1e6 for t in times], "o-", linewidth=1.5, markersize=4)
    ax1.set_xlabel("n")
    ax1.set_ylabel("Temps moyen (µs)")
    ax1.set_title("Temps vs n")
    ax1.grid(True)

    ax2.plot(log_n, log_t, "o", markersize=4, label="mesures")
    ax2.plot(log_n, slope * log_n + intercept, "--",
             label=f"pente = {slope:.2f}")
    ax2.set_xlabel("log(n)")
    ax2.set_ylabel("log(temps)")
    ax2.set_title("log-log → pente ≈ ")
    ax2.legend()
    ax2.grid(True)

    # Temps vs b : courbe exponentielle (semi-log doit être une droite)
    ax3.semilogy(bits, [t * 1e6 for t in times], "o-", linewidth=1.5, markersize=4,
                 label="mesures")
    b_fit = np.array([min(bits), max(bits)])
    ax3.semilogy(b_fit, np.exp(slope_b * b_fit + intercept_b) * 1e6, "--",
                 label=f"régression : pente = {slope_b:.4f}\n(attendu {math.log(2)/2:.4f})")
    ax3.set_xlabel("b = ⌊log₂(n)⌋  (nombre de bits)")
    ax3.set_ylabel("Temps moyen (µs)  [échelle log]")
    ax3.set_title("Temps vs b — exponentiel en b")
    ax3.legend()
    ax3.grid(True, which="both")

    plt.tight_layout()
    out = "td2/complexity_fermat_primality.png"
    plt.savefig(out, dpi=150)
    print(f"Graphique sauvegardé : {out}")
    plt.show()


if __name__ == "__main__":
    run()
