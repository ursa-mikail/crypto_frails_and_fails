#!pip install pycryptodome gmpy2
import Crypto.Util.number as cun
from sympy.ntheory.modular import crt
from gmpy2 import iroot

# Step 1: Generate three RSA public keys (e=3)
e = 3
keys = []
for _ in range(3):
    p = cun.getPrime(512)
    q = cun.getPrime(512)
    n = p * q
    keys.append(n)

# Step 2: Encrypt the same plaintext under all 3 keys
plaintext = b"HastadAttack"
m = int.from_bytes(plaintext, 'big')

assert all(m < n for n in keys), "Message must be smaller than each modulus"

ciphers = [pow(m, e, n) for n in keys]

# Step 3: Apply Chinese Remainder Theorem to recover m^e
M, _ = crt(keys, ciphers)  # M ≡ m^3 mod (n1 * n2 * n3)

# Step 4: Take integer cube root of M to recover m
m_recovered, exact = iroot(M, e)
assert exact, "Cube root not exact; attack conditions not met"

# Step 5: Decode recovered message
recovered = int.to_bytes(int(m_recovered), len(plaintext), 'big')
print("Recovered plaintext:", recovered)

# ❌ Demonstration: Håstad’s Attack Failure Case
import Crypto.Util.number as cun
from sympy.ntheory.modular import crt
from gmpy2 import iroot, mpz

# Step 1: Generate three RSA public keys (e = 3)
e = 3
keys = []
for _ in range(3):
    p = cun.getPrime(512)
    q = cun.getPrime(512)
    n = p * q
    keys.append(n)

N_product = keys[0] * keys[1] * keys[2]

# Step 2: Compute cube root of N_product using gmpy2
N_root, _ = iroot(mpz(N_product), 3)
m = N_root + 1000  # Ensure m^3 > N_product

# Step 3: Encrypt the same plaintext
ciphers = [pow(m, e, n) for n in keys]

# Step 4: Use Chinese Remainder Theorem to get m^3 mod N
M, _ = crt(keys, ciphers)

# Step 5: Try to take cube root of M
m_recovered, exact = iroot(M, e)

# Step 6: Output
print("Was the cube root exact?", exact)
print("Original message:     ", m)
print("Recovered message:    ", int(m_recovered))

if not exact or int(m_recovered) != m:
    print("❌ Attack failed: recovered message is incorrect.")
else:
    print("✅ Attack succeeded: recovered message is correct.")

"""
Recovered plaintext: b'HastadAttack'

Was the cube root exact? False
Original message:      134720944716171461563076742902790918554412320420630514421235258148293184276340719683264119512945418975356557901541245904177211190211899170516247700176289022986801352213321415428155283752999274379859304800715923362708554491646682165218100623041371096878727680502103015362398465275079703202012493683433142319002
Recovered message:     378914307121708311521331879042789416502937201147677075849330173442432856536417305388627076952958268039025383246160303471653179280312016289557179708497358064122994386409235794992502439666372225091081269546873
❌ Attack failed: recovered message is incorrect.
"""