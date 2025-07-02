#!pip install gmpy2

import gmpy2
from gmpy2 import mpz
import random

def random_512_bit_int():
    return mpz(random.getrandbits(512))

def experiment(n):
    total = 0
    for _ in range(n):
        p = random_512_bit_int()
        if gmpy2.is_prime(p):
            total += 1
    return total

if __name__ == "__main__":
    sample_size = 10000
    num_primes = experiment(sample_size)
    print(f"Out of {sample_size} random 512-bit integers, {num_primes} are prime.")
    print(f"Estimated probability ≈ {num_primes / sample_size:.5f}")

"""
Successfully installed gmpy2-2.2.1
Out of 10000 random 512-bit integers, 19 are prime.
Estimated probability ≈ 0.00190
"""