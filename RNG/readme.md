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


1. On the client side, during RSA handshake. RNG is used to generate RSA pre-master secret and encryption padding. If the attacker can predict the output of this generator, she can subsequently decrypt the entire session. Ironically, a failure of the server RNG is less devastating to the RSA handshake.
2. On the client or server side, during the Diffie-Hellman handshake(s). Since Diffie-Hellman requires a contribution from each side of the connection, a predictable RNG on either side renders the session completely transparent.
3. During long-term key generation, particularly of RSA keys. If this happens, it's over.

### On salt as a randomizer:

The purpose of including salts is to modify the function used to hash each user's password so that each stored password hash will have to be attacked individually. The only security requirement is that they are unique per user, there is no benefit in them being unpredictable or difficult to guess.

Salts only need to be long enough so that each user's salt will be unique. Random 64-bit salts are unlikely to ever repeat even with a billion registered users. A singly repeated salt is a relatively minor security concern, it allows an attacker to search 2 accounts at once but in the aggregate won't speed up the search much on the whole database. Even 32-bit salts are acceptable for most purposes, it will in the worst case speed an attacker's search by about 58%. The cost of increasing salts beyond 64 bits isn't high but there is no security reason to do so. There is benefit to also using a site-wide salt on top of the per-user salt, this will prevent possible collisions with password hashes stored at other sites, and prevent the use of general-purpose rainbow tables, although even 32 bits of salt is enough to make rainbow tables an impractical attack.


