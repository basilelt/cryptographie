# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 12:22:34 2024

@author: JDION
"""

import matplotlib.pyplot as plt
import random

from math import gcd
from sympy import isprime

"""
GENERATION DE NB PREMIER SELON TEST DE PRIMALITE DE FERMAT
"""


def is_prime_fermat(n, k=100):
    """
    Teste si n est premier
    """
    if n <= 1:
        return False
    if n == 2:
        return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False

    return True


def generate_prime(start, end, test_function):
    """
    Génère un nombre premier dans l'intervalle [start, end] à partir d'un test personnalisé
    """
    while True:
        candidate = random.randint(start, end)
        if test_function:
            if test_function(candidate):
                return candidate


"""
EXERCICE 2
"""


def generate_safe_prime(bits: int) -> tuple[int, int]:
    low, high = 2 ** (bits - 1), 2**bits - 1
    while True:
        q = generate_prime(low, high, is_prime_fermat)
        p = 2 * q + 1
        if is_prime_fermat(p):
            return p, q


def find_generator(p: int, q: int) -> int:
    while True:
        g = random.randint(2, p - 2)
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            return g


def diffie_hellman(bits: int = 16) -> tuple[int, int, int, int, int]:
    p, q = generate_safe_prime(bits)
    g = find_generator(p, q)

    a = random.randint(2, p - 2)
    b = random.randint(2, p - 2)
    A = pow(g, a, p)
    B = pow(g, b, p)

    K_alice = pow(B, a, p)
    K_bob = pow(A, b, p)
    assert K_alice == K_bob

    return p, g, A, B, K_alice

# See @td1/vigenere.py for the Vigenère cipher implementation
def vigenere_decrypt(message: str, key: str) -> str:
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


"""
EXERCICE 3
"""


"""
EXERCICE 4
"""


def elliptic_curve_points(a, b, p):
    """
    Liste les points de la courbe elliptique y^2 = x^3 + ax + b sur le corps fini Z/pZ.

    :param a: Coefficient a de la courbe elliptique
    :param b: Coefficient b de la courbe elliptique
    :param p: Nombre premier définissant le corps fini Z/pZ
    :return: Une liste de tuples représentant les points (x, y) de la courbe elliptique,
             ainsi que le point à l'infini (indiqué par "INF").
    """

    def is_quadratic_residue(value, p):
        """
        Vérifie si 'value' est un résidu quadratique modulo p (a un carré modulo p).
        """
        if value == 0:
            return True
        return pow(value, (p - 1) // 2, p) == 1

    def sqrt_mod(value, p):
        """
        Trouve une racine carrée de 'value' modulo p (si elle existe).
        Utilise une méthode rapide pour p ≡ 3 (mod 4), et l'algorithme de Tonelli-Shanks sinon.
        """
        if not is_quadratic_residue(value, p):
            return None

        if p % 4 == 3:
            return pow(value, (p + 1) // 4, p)

        # Algorithme de Tonelli-Shanks pour p ≡ 1 (mod 4)
        # Étape 1 : Trouver q et s tels que p - 1 = q * 2^s avec q impair
        q, s = p - 1, 0
        while q % 2 == 0:
            q //= 2
            s += 1

        # Étape 2 : Trouver un non-résidu quadratique z mod p
        z = 2
        while is_quadratic_residue(z, p):
            z += 1

        # Initialisation des variables
        m = s
        c = pow(z, q, p)
        t = pow(value, q, p)
        r = pow(value, (q + 1) // 2, p)

        # Boucle de Tonelli-Shanks
        while t != 0 and t != 1:
            t2i = t
            i = 0
            for i in range(1, m):
                t2i = pow(t2i, 2, p)
                if t2i == 1:
                    break

            b = pow(c, 2 ** (m - i - 1), p)
            m = i
            c = pow(b, 2, p)
            t = (t * c) % p
            r = (r * b) % p

        return r if t == 1 else None

    points = []

    for x in range(p):
        # Calcule le côté droit de l'équation : x^3 + ax + b mod p
        rhs = (x**3 + a * x + b) % p

        # Vérifie si rhs est un résidu quadratique mod p
        if is_quadratic_residue(rhs, p):
            # Trouve les racines y telles que y^2 = rhs mod p
            y = sqrt_mod(rhs, p)
            if y is not None:
                points.append((x, y))
                # Ajoute aussi le point opposé (x, -y mod p)
                if y != 0:
                    points.append((x, p - y))

    # Ajoute le point à l'infini (noté "INF")
    points.append("INF")

    return points


def plot_elliptic_curve(a, b, p):
    """
    Représente graphiquement les points d'une courbe elliptique sur un corps fini Z/pZ.

    :param a: Coefficient a de la courbe elliptique
    :param b: Coefficient b de la courbe elliptique
    :param p: Nombre premier définissant le corps fini Z/pZ
    """

    points = elliptic_curve_points(a, b, p)
    finite_points = [(x, y) for point in points if point != "INF" for x, y in [point]]

    x_vals, y_vals = zip(*finite_points)

    plt.scatter(x_vals, y_vals, c="blue", label="Points sur la courbe")
    plt.title(f"Courbe elliptique: y^2 = x^3 + {a}x + {b} mod {p}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-0.5, p - 0.5)
    plt.ylim(-0.5, p - 0.5)
    plt.grid(True)
    plt.legend()
    plt.show()


def add_points(P, Q, a, p):
    """
    Effectue l'addition de deux points P et Q sur une courbe elliptique.

    :param P: Point P sous la forme (x1, y1) ou "INF" pour le point à l'infini
    :param Q: Point Q sous la forme (x2, y2) ou "INF" pour le point à l'infini
    :param a: Coefficient a de la courbe elliptique
    :param p: Nombre premier définissant le corps fini Z/pZ
    :return: Le résultat de P + Q sous la forme d'un tuple (x, y) ou "INF"
    """
    if P == "INF":
        return Q
    if Q == "INF":
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % p == 0:
        return "INF"  # P et Q sont opposés, donc P + Q = INF

    if P == Q:
        # Cas de la tangente : lambda = (3x1^2 + a) / (2y1) mod p
        num = (3 * x1**2 + a) % p
        den = pow(2 * y1, -1, p)
    else:
        # Cas de la sécante : lambda = (y2 - y1) / (x2 - x1) mod p
        num = (y2 - y1) % p
        den = pow(x2 - x1, -1, p)

    lamb = (num * den) % p

    # Calcul des coordonnées du résultat
    x3 = (lamb**2 - x1 - x2) % p
    y3 = (lamb * (x1 - x3) - y1) % p

    return (x3, y3)


def get_generator(a, b, p):
    """
    Trouve un générateur de la courbe elliptique y^2 = x^3 + ax + b sur Z/pZ.
    Un générateur est un point qui engendre tous les points de la courbe par addition.

    :param a: Coefficient a de la courbe elliptique
    :param b: Coefficient b de la courbe elliptique
    :param p: Nombre premier définissant le corps fini Z/pZ
    :return: Un générateur (x, y) ou None si aucun n'est trouvé
    """
    points = elliptic_curve_points(a, b, p)
    finite_points = [P for P in points if P != "INF"]  # Exclure le point à l'infini

    for P in finite_points:
        # Génère tous les multiples de P
        generated_points = set()
        Q = P
        for _ in range(len(finite_points)):
            generated_points.add(Q)
            Q = add_points(Q, P, a, p)  # Additionner P à lui-même

        # Inclure le point à l'infini pour vérifier si c'est un générateur
        generated_points.add("INF")

        if generated_points == set(points):
            return P

    return None


def scalar_multiplication(k, P, a, p):
    """
    Effectue une multiplication scalaire k * P sur la courbe elliptique.
    Utilise l'algorithme de doublement et ajout (double-and-add).
    """
    result = "INF"  # Point à l'infini
    temp = P

    while k > 0:
        if k % 2 == 1:
            result = add_points(result, temp, a, p)
        temp = add_points(temp, temp, a, p)
        k //= 2

    return result


if __name__ == "__main__":
    # Exercice 2 - attaque par brute force (log discret) : p=467, g=2, A=228, B=57
    p_att, g_att, A_att, B_att = 467, 2, 228, 57
    ct = "GRHTTXKRJTHRI"

    a_att = next(x for x in range(1, p_att - 1) if pow(g_att, x, p_att) == A_att)
    K_att = pow(B_att, a_att, p_att)
    # chiffres de K convertis en lettres : 0→A, 1→B, ..., 9→J
    key_att = "".join(chr(ord("A") + int(d)) for d in str(K_att))
    pt = vigenere_decrypt(ct, key_att)

    print(f"\n--- Attaque ---")
    print(f"a = {a_att}, K = {K_att}")
    print(f"Clé Vigenère : {key_att}")
    print(f"Message déchiffré : {pt}")
    
    
    # Exercice x
