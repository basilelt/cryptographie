import math

# Est premier si il n'est divisible que par 1 et lui même
def is_prime_naive(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if sum([int(digit) for digit in str(n)]) % 9 == 0:
        return False

    # On teste les diviseurs impaires de 3 à sqrt(n)
    for d in range(3, math.isqrt(n) + 1, 2):
        if n % d == 0:
            return False
    return True

if __name__ == "__main__":
    primes   = [2, 3, 5, 7, 11, 13, 97, 101, 7919]
    composites = [1, 4, 9, 15, 100, 7920, 648923754902735, 4328947329865, 876545678]
    print(list(is_prime_naive(p) for p in primes))
    print(list(is_prime_naive(c) for c in composites))

