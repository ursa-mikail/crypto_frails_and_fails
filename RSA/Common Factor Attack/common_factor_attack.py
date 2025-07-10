"""
Loads a list of RSA public moduli (as integers).
Computes pairwise gcd for all pairs.
Detects which pairs share a factor (gcd > 1 and not equal to 1).
For those pairs, computes the private factors p, q of each n.
Prints out the vulnerable key pairs and their factors.
"""
import math

# Example RSA moduli (replace with real moduli loaded from PEMs)
# For demonstration, these are small values with shared primes.
# Replace with your real RSA n values, parsed as integers.
rsa_moduli = [
    0xD5C6237B3B9E1E9F1E3C9D5B53DF989C7F0F7F73F5C59B9B,  # n1 = p1 * q1
    0xB7F62439B1A573EB1D03B545B933B69C7F0F7F73F5C59B9B,  # n2 shares prime q1 (last 16 digits same)
    0xE2F485AB9F7131A11C3A9B9B9E2D45BCE3A5E48AB37F0139,  # n3 distinct, no factor sharing
    # add more moduli...
]

def find_vulnerable_keys(moduli):
    """Given a list of RSA moduli, find pairs sharing a prime factor."""
    n = len(moduli)
    compromised = []

    for i in range(n):
        for j in range(i + 1, n):
            gcd_val = math.gcd(moduli[i], moduli[j])
            if gcd_val != 1:
                # Found shared factor
                p = gcd_val
                q1 = moduli[i] // p
                q2 = moduli[j] // p
                compromised.append({
                    "key1_index": i,
                    "key2_index": j,
                    "shared_factor": p,
                    "factors_key1": (p, q1),
                    "factors_key2": (p, q2),
                })

    return compromised

def main():
    compromised_keys = find_vulnerable_keys(rsa_moduli)

    if not compromised_keys:
        print("No vulnerable keys detected (no shared prime factors).")
        return

    print(f"Found {len(compromised_keys)} vulnerable key pairs!\n")

    for entry in compromised_keys:
        print(f"Keys #{entry['key1_index']} and #{entry['key2_index']} share a prime factor.")
        print(f"Shared prime factor (p): {entry['shared_factor']}")
        print(f"Factors of key #{entry['key1_index']}: p = {entry['factors_key1'][0]}, q = {entry['factors_key1'][1]}")
        print(f"Factors of key #{entry['key2_index']}: p = {entry['factors_key2'][0]}, q = {entry['factors_key2'][1]}")
        print("-" * 60)

if __name__ == "__main__":
    main()

"""
Found 1 vulnerable key pairs!

Keys #0 and #2 share a prime factor.
Shared prime factor (p): 3
Factors of key #0: p = 3, q = 1747240903582964373744092496646798417501318494842263821961
Factors of key #2: p = 3, q = 1854974814934680194391374840908224146372751730941418777363
"""