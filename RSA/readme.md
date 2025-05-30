# Håstad’s Broadcast Attack on RSA with a small exponent (e = 3). 

This attack works when:

The same plaintext `m` is encrypted with e = 3 under 3 different RSA public keys `(n1, e)`, `(n2, e)`, `(n3, e)`

All ciphertexts are intercepted: `c1 = m^3 mod n1`, `c2 = m^3 mod n2`, `c3 = m^3 mod n3`

The `n`s are pairwise coprime.

The message `m` is small enough that `m^3 < n1 * n2 * n3`, so Chinese Remainder Theorem (CRT) can be used to recover `m^3`, and cube root gives `m`.

CRT aggregates the 3 ciphertexts into a single congruence that reveals m^3.

iroot from gmpy2 efficiently computes the integer cube root of m^3.

Since m^3 is less than the product of the moduli, it recovers the exact m.

## When `m^3 < n1 * n2 * n3 is not met`
Håstad's attack fails when the condition m^3 < n1 * n2 * n3 is not met — that is, when the plaintext is too large.

In this case:
CRT still reconstructs m^3 mod N, but since m^3 ≥ N, the result wraps around modulo N, and the cube root gives the wrong result.

You cannot recover the original message

| Condition            | Attack Works? |
| -------------------- | ------------- |
| `m^e < n1 * n2 * n3` | ✅ Yes         |
| `m^e ≥ n1 * n2 * n3` | ❌ No          |

