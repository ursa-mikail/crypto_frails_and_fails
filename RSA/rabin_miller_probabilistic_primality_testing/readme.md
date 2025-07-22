# 🔐 Rabin-Miller Prime Generator (Python)
This tool generates large probable prime numbers using the Rabin-Miller primality test, a widely-used algorithm in cryptography (e.g., RSA key generation).

It’s implemented in Python using cryptographically secure randomness (secrets) and customizable for any bit size (e.g. 512, 1024, 2048).

```
📦 Features
✅ Bit-size control (e.g. 512, 1024, 2048 bits)

✅ Secure randomness with secrets (safer than random)

✅ Rabin-Miller primality test (configurable rounds)

✅ Fully self-contained and easy to use
```

## ✨ What Is a "Probable Prime"?
A probable prime is a number that passes a series of mathematical tests that very strongly suggest it is prime — though not guaranteed. The Rabin-Miller test makes this error probability exponentially small with each round.

In practice: With 40 rounds, the chance of a composite number passing all tests is less than 1 in 2⁸⁰, which is extremely secure for cryptographic use.

## 🧪 How It Works
1. Rabin-Miller Test:
- Writes $$\ n−1 = 2^r ⋅ d \$$
- Randomly picks base a and tests whether $$\ a^d \$$ mod n and its powers indicate primality.
- Repeats k times (more rounds = more certainty).
- If any round fails → n is **composite`.

2. Prime Generation:
- Randomly generates an odd number of desired bit length
- Checks if it’s a probable prime
- Repeats until one is found

| Step | What Happens                                                |
| ---- | ----------------------------------------------------------- |
| 1    | Handle small cases and rule out even numbers                |
| 2    | Express $n - 1 = 2^r \cdot d$                               |
| 3    | Pick random base $a$, check if $a^d \mod n = 1$ or $n-1$    |
| 4    | If not, square repeatedly to check if $x \rightarrow n - 1$ |
| 5    | If no round fails → **probably prime**                      |
| 6    | If any round fails → **definitely composite**               |


Although Rabin-Miller is a **probabilistic** test (not 100% guaranteed), it’s **extremely safe** for cryptographic use. Here's why:

### 🔐 1. Exponentially small error rate

- Each test round reduces the chance of a composite number passing as prime by at least 75%.
- After `k` rounds, the chance of error is at most:

  \[
  \left(\frac{1}{4}\right)^k
  \]

- With `k = 40`, the probability of a false positive is:

  \[
  < 9 \times 10^{-25}
  \]

  That’s astronomically small — much smaller than hardware bit flip error rates.

---
