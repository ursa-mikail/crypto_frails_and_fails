# Prime Density Estimator by Bit Size

This Python script estimates the number of prime numbers between `2^(n-1)` and `2^n` for a range of bit sizes using the **Riemann R function**. It also plots the **probability of randomly selecting a prime number** in that range.

## 📌 Features

- Estimates prime counts using the Riemann prime counting function `R(x)`
- Computes probability of randomly selecting a prime in a given bit-length range
- Batch analysis for bit sizes (default: 128 to 2048)
- Plots prime density vs. bit size using `matplotlib`

---

## 🧠 Background

In cryptography we sometimes have to estimate pi(x) , and which is the number of primes between 0 and x . This page estimate the number of primes for a given bit size and will use the Riemannr method.

One method which can be used to estimate the number of prime numbers is the Riemann R function. This is a smooth approximation for π(x). The function is defined using the rapidly convergent Gram series:

$$\ R(x) = 1 + \sum^{\inf}_{k=1} \frac{\log^k x}{ k.k! \zeta (k+1) } \$$

The number of primes less than a number `x` can be estimated using the Riemann R function:

$$\ π(x) ≈ R(x) \$$


To find the number of primes in a bit range:

$$\ Count ≈ R(2^n) - R(2^(n-1)) \$$


Probability is computed as:

$$\ P(n) = (Estimated primes in range) / (Total numbers in range) × 100% \$$

Number of bits in prime number:	512
Estimated number of prime numbers:	961409783
Chance of finding a prime:		6.61 %

### ⚙️ Customize Range

```

To change the range or step size, modify:
generate_probability_plot(start_bits=128, end_bits=2048, step=128)

For example, to go from 256 to 1024 with 64-bit steps:
generate_probability_plot(start_bits=256, end_bits=1024, step=64)
```
