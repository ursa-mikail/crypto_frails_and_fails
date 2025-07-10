# Fermat Factorization Attack on RSA

This project demonstrates how **Fermat's Factorization Method** can be used to break RSA when the two prime factors of the modulus `n = p * q` are **too close to each other**.

## 🔓 Why This Matters

Fermat's method is efficient when the difference between the primes `p` and `q` is small. If an RSA implementation mistakenly chooses `p` and `q` that are close in value, an attacker can factor `n` quickly, thus **breaking the RSA key**.

---

## ✅ What This Code Demonstrates

- Case 1: `p` and `q` are close — **Fermat can factor `n`** successfully.
- Case 2: `p` and `q` are random — Fermat usually **fails to factor `n`**.

## 🔬 How Fermat Factorization Works
Fermat’s method is based on the identity:

```
n = a² - b² = (a + b)(a - b)
```
We then have the first prime as a−b and the second one as a+b. 
If the prime numbers are close then the value of a will be close to the square root of N. We could thus guess the value of a from the square root of N and then increment the value of a and for each guess we take:
```
b² = a² - n
```
If you can find a such that a² - n is a perfect square, then:

```
p = a + b  
q = a - b
```
This is easy if p and q are close together because a = ceil(sqrt(n)) will be very close to p.

## ⚠️ Security Warning
Do not use RSA with small differences between p and q. Always ensure:
```
|p - q| is large enough

p and q are generated independently

RSA key generation uses secure libraries
```

```
Prime number size: 512 bits

== Try with p and q close to each other (within 2^20) ==
N = ...
[SUCCESS] Fermat was able to factor n.
Factors: p = ..., q = ...

== Try with p and q as random primes ==
N = ...
[FAILURE] Fermat failed to factor n.
```

---

## 🧠 Requirements

- Python 3
- `gmpy2` library for fast math operations

Install the dependency:
```bash
pip install gmpy2

