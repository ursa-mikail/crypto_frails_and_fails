# rabin_miller_probabilistic_primality_testing
import secrets


def is_probable_prime(n: int, k: int = 40) -> bool:
    """
    Perform Rabin-Miller primality test.
    n: number to test for primality.
    k: number of testing rounds (higher = stronger confidence).
    Returns True if n is probably prime, False if composite.
    """
    if n in (2, 3):             # Special case: 2 and 3 are small primes, return True
        return True
    if n <= 1 or n % 2 == 0:    # Any number less than 2 or even (other than 2) is not prime.
        return False

    # Write n-1 as 2^r * d. Essential to prepare for the Miller-Rabin test.
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Repeat test k times
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # pick random a in [2, n-2]. Randomly choose a base 𝑎 a such that 2 ≤ 𝑎 ≤ 𝑛 − 2 
        x = pow(a, d, n)        # 𝑎^𝑑 mod 𝑛 

        if x == 1 or x == n - 1:
            continue  # maybe prime
        # Square 𝑥 up to 𝑟 − 1 times 
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break  # maybe prime
        else:
            return False  # definitely composite

    return True  # probably prime


def generate_prime(bits: int, k: int = 40) -> int:
    """
    Generate a random probable prime number of given bit size.
    Uses Rabin-Miller test for primality check.
    """
    while True:
        # Generate odd random number with highest bit set
        candidate = secrets.randbits(bits)
        candidate |= (1 << bits - 1) | 1  # Ensure it's odd and has correct bit length

        if is_probable_prime(candidate, k):
            return candidate


if __name__ == "__main__":
    bit_length = 512  # Change to 1024, 2048, etc. for stronger keys
    print(f"Generating a probable prime of {bit_length} bits...")
    prime = generate_prime(bit_length)
    print("Generated prime:")
    print(prime)

"""
Generating a probable prime of 512 bits...
Generated prime:
11739097932897431100563035629563986053844067785188818967790781873449195349828288093984519144910349899612391927304219011193103894041198099033723684691907223

"""
