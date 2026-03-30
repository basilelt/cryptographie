"""
Étude expérimentale de la complexité du test de primalité naïf.
"""

import math
import time
import numpy as np
import matplotlib.pyplot as plt

from main import is_prime_naive


def next_prime(start: int) -> int:
    """Retourne le plus petit premier >= start."""
    n = start | 1  # force impair
    while not is_prime_naive(n):
        n += 2
    return n


def measure(n: int, repeats: int = 30) -> float:
    """Temps moyen (s) pour tester la primalité de n."""
    t0 = time.perf_counter()
    for _ in range(repeats):
        is_prime_naive(n)
    return (time.perf_counter() - t0) / repeats


def run():
    # Pire cas : n premier → on parcourt tous les diviseurs jusqu'à √n
    # Valeurs logarithmiquement espacées entre 10^1 et 10^8
    ns_raw = np.logspace(1, 8, num=40, dtype=int)
    candidates = [next_prime(int(n)) for n in ns_raw]
    times = [measure(n) for n in candidates]
    sqrts = [math.sqrt(n) for n in candidates]

    # --- Tableau ---
    print(f"{'n':>12}  {'√n':>10}  {'temps (µs)':>12}")
    print("-" * 38)
    for n, sq, t in zip(candidates, sqrts, times):
        print(f"{n:>12}  {sq:>10.1f}  {t*1e6:>12.4f}")

    # --- Régression log-log (en fonction de n) ---
    log_n = np.log(candidates)
    log_t = np.log(times)
    slope, intercept = np.polyfit(log_n, log_t, 1)
    print(f"\nPente log-log = {slope:.3f}  (attendu ≈ 0.5 pour Θ(√n))")

    # --- Graphiques ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    ax1.plot(candidates, [t * 1e6 for t in times], "o-", linewidth=1.5, markersize=4)
    ax1.set_xlabel("n")
    ax1.set_ylabel("Temps moyen (µs)")
    ax1.set_title("Temps vs n  —  pire cas (n premier)")
    ax1.grid(True)

    ax2.plot(log_n, log_t, "o", markersize=4, label="mesures")
    ax2.plot(log_n, slope * log_n + intercept, "--",
             label=f"régression : pente = {slope:.2f}")
    ax2.set_xlabel("log(n)")
    ax2.set_ylabel("log(temps)")
    ax2.set_title("Graphe log-log → pente ≈ 0.5 confirme Θ(√n)")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    out = "td2/complexity_naive_primality.png"
    plt.savefig(out, dpi=150)
    print(f"Graphique sauvegardé : {out}")
    plt.show()


if __name__ == "__main__":
    run()
