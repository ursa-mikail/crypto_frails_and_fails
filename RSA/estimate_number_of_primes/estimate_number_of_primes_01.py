import matplotlib.pyplot as plt
from mpmath import riemannr
from decimal import Decimal, getcontext

getcontext().prec = 100


def sieve(n: int):
    if n < 2:
        return []
    sieve_arr = [True] * (n + 1)
    sieve_arr[0] = sieve_arr[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if sieve_arr[p]:
            for multiple in range(p * p, n + 1, p):
                sieve_arr[multiple] = False
    return [i for i, is_prime in enumerate(sieve_arr) if is_prime]


def exact_pi(n: int) -> int:
    return len(sieve(n))


def estimate_pi(n: int) -> int:
    return int(riemannr(n))


def to_scientific_notation(n: int, precision: int = 3) -> str:
    if n == 0:
        return "0"
    d = Decimal(n)
    exponent = d.adjusted()
    mantissa = d.scaleb(-exponent).normalize()
    return f"{mantissa:.{precision}f}×10^{exponent}"


def main():
    print("Prime counting: exact vs Riemann R estimation\n")

    powers = list(range(1, 8))  # 10^1 to 10^7
    exact_counts = []
    riemann_counts = []

    for p in powers:
        n = 10 ** p
        print(f"Range: 1 to {n}")

        exact = exact_pi(n)
        est = estimate_pi(n)

        exact_counts.append(exact)
        riemann_counts.append(est)

        # Calculate probability of prime in that range (1 to n)
        prob = (exact / n) * 100

        print(f"Estimation of primes:\t\t\t{exact}")
        print(f"Possibility of finding prime (%):\t{prob:.4f}\n")

        exact_str = to_scientific_notation(exact)
        est_str = to_scientific_notation(est)
        print(f"10^{p}:\tExact π(n) = {exact_str}\tEstimated π(n) = {est_str}\n")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(powers, riemann_counts, 'o-', label='Riemann R Estimate', color='blue')
    plt.plot(powers, exact_counts, 's--', label='Exact Count (sieve)', color='red')

    plt.xticks(powers, [f"10^{p}" for p in powers])
    plt.yscale('log')
    plt.xlabel("n")
    plt.ylabel("Number of primes ≤ n (log scale)")
    plt.title("Exact vs Estimated Prime Counting Function π(n)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

"""
# Eratosthenes sieve

Prime counting: exact vs Riemann R estimation

Range: 1 to 10
Estimation of primes:           4
Possibility of finding prime (%):   40.0000

10^1:   Exact π(n) = 4.000×10^0 Estimated π(n) = 4.000×10^0

Range: 1 to 100
Estimation of primes:           25
Possibility of finding prime (%):   25.0000

10^2:   Exact π(n) = 2.500×10^1 Estimated π(n) = 2.500×10^1

Range: 1 to 1000
Estimation of primes:           168
Possibility of finding prime (%):   16.8000

10^3:   Exact π(n) = 1.680×10^2 Estimated π(n) = 1.680×10^2

Range: 1 to 10000
Estimation of primes:           1229
Possibility of finding prime (%):   12.2900

10^4:   Exact π(n) = 1.229×10^3 Estimated π(n) = 1.226×10^3

Range: 1 to 100000
Estimation of primes:           9592
Possibility of finding prime (%):   9.5920

10^5:   Exact π(n) = 9.592×10^3 Estimated π(n) = 9.587×10^3

Range: 1 to 1000000
Estimation of primes:           78498
Possibility of finding prime (%):   7.8498

10^6:   Exact π(n) = 7.850×10^4 Estimated π(n) = 7.853×10^4

Range: 1 to 10000000
Estimation of primes:           664579
Possibility of finding prime (%):   6.6458

10^7:   Exact π(n) = 6.646×10^5 Estimated π(n) = 6.647×10^5
"""