import math
import random

# Est premier si il n'est divisible que par 1 et lui même
def is_prime_fermat(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if sum([int(digit) for digit in str(n)]) % 9 == 0:
        return False
    
    a = random.randint(2, n-1)
    if pow(a, n-1, n) == 1:
        return True

    return False

    
if __name__ == "__main__":
    primes   = [2, 3, 5, 7, 11, 13, 97, 101]
    composites = [1, 4, 9, 15, 100]
    print(list(is_prime_fermat(p) for p in primes))
    print(list(is_prime_fermat(c) for c in composites))

