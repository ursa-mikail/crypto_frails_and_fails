import math

def fermat_factor(n):
    """Performs Fermat's factorization on n = p*q.
    Assumes p and q are odd and close together."""
    assert n % 2 != 0, "Fermat's method works best when n is odd"

    t = math.isqrt(n) + 1
    steps = 0

    while True:
        x_squared = t * t - n
        x = math.isqrt(x_squared)
        if x * x == x_squared:
            p = t + x
            q = t - x
            return (p, q, steps)
        t += 1
        steps += 1

def verify_fermat_steps(p, q):
    """Show Fermat will take at most (p - q)//2 + 1 steps"""
    diff = abs(p - q)
    return diff // 2 + 1

if __name__ == "__main__":
    n = 23360947609
    print(f"Trying to factor n = {n} using Fermat's method...\n")

    p, q, steps = fermat_factor(n)

    print(f"Success! Factors found:")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"Steps taken = {steps}")

    theoretical_bound = verify_fermat_steps(p, q)
    print(f"\nTheoretical maximum steps = (p - q) // 2 + 1 = {theoretical_bound}")
    print(f"{'✔️ Success within bound!' if steps <= theoretical_bound else '❌ Exceeded theoretical bound!'}")

"""
Trying to factor n = 23360947609 using Fermat's method...

Success! Factors found:
p = 153649
q = 152041
Steps taken = 2

Theoretical maximum steps = (p - q) // 2 + 1 = 805
✔️ Success within bound!
"""