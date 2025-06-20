# Weak PRNG In The Midst

## Broken Randomness 

Flaw at insuring the property that all of the polynomial coefficients but the secret are chosen at random (esp for Shamir Sharing), e.g. if you use hash (secret), rainbow attack can find the secret.

e.g.  non-randomness of the polynomial coefficients — specifically when some coefficients are deterministically derived from the secret, such as via hashing, instead of being chosen uniformly at random. 

⚠️ Flaw in Polynomial Construction in Shamir's Secret Sharing
In Shamir’s Secret Sharing, a secret s is split among participants by constructing a random polynomial f(x) of degree t-1, where t is the reconstruction threshold:

$$\ f(x)=a_0​+ a_1​x + a_2​x^2 +⋯+ a_{t−1}​x^{t−1} \$$

- a_0 = s is the secret
- The remaining coefficients a_1 to a_{t-1} must be uniformly random over the finite field

❌ What Goes Wrong If You Use hash(secret) or Other Deterministic Values?
Some flawed implementations try to "simplify" or "bind" the polynomial to the secret by doing something like:

```python
a_1 = H(secret)
a_2 = H(H(secret))
...
```
Or:

```python

a_1 = PRNG(seed=H(secret)).next()
```

While this does not break the mathematical reconstruction of SSS, it introduces a major cryptographic flaw:

🔓 Why Is This Dangerous? (Rainbow Table / Preimage Attacks)
If an attacker knows:

- The mechanism used to derive coefficients from the secret (e.g., a_1 = H(secret)), and
- One or more shares,

Then:
- The attacker can brute-force candidate secrets, checking each one by regenerating the derived polynomial and testing it against known shares.

In this case:
- The entropy of the secret s alone becomes the sole barrier to a brute-force attack — which is weak if the secret is, for instance, a password or a short string.

This is effectively a rainbow table or preimage attack:
- Precompute (secret_candidate, share_output) pairs
- Compare against a leaked share to recover the secret


✅ Correct Practice: Use High-Entropy Random Coefficients
In proper SSS:

Only a_0 is tied to the secret.

All a_1 to a_{t-1} must be generated using a cryptographically secure random number generator (CSPRNG), independent of the secret.

This guarantees:
- The shares reveal no information about the secret unless t or more are combined.
- Even with one share, the secret is information-theoretically secure.

| Practice                    | Description                                 | Security                                       |
| --------------------------- | ------------------------------------------- | ---------------------------------------------- |
| ✅ `a_i = random()`          | All coefficients (except secret) are random | Secure                                         |
| ❌ `a_i = hash(secret)`      | Coefficients derived from secret            | Vulnerable to brute-force and preimage attacks |
| ❌ `a_i = PRNG(seed=secret)` | Deterministic based on secret               | Leaks structure, weakens hiding property       |

🔁 Real-World Parallel
This flaw is similar to using a non-random IV in encryption or using H(password) directly as an encryption key — the deterministic pattern breaks the semantic security of the system.



## Broken Randomness: RNG

Using PRNG without entropy testing and uninitialized seed or constant seed or seed not securing stored. 

🔓 Scenario
Simulate a weak PRNG-based AES encryption system:

- The key is generated using rand() seeded with a low-entropy value (e.g., system time).
- Attacker who knows or guesses the time window can brute-force the seed.
- Attacker regenerates the key, decrypts the ciphertext, and recovers the plaintext.

<hr>
A low-entropy PRNG seed (like time() or PID) used to generate cryptographic keys is vulnerable.

Brute-forcing the seed within a reasonable window (e.g., ±60 seconds) is very feasible.

This kind of flaw has been seen in the wild (e.g., Bitcoin wallet vulnerabilities, embedded device key generation flaws, etc.)

### Caveats
Never use predictable seeds (e.g., time) for key generation.

Use a cryptographically secure RNG, e.g., os.urandom(), secrets, or /dev/urandom.

Always ensure IVs are random and unique per encryption when using CBC mode.

