# Weak PRNG In The Midst

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

