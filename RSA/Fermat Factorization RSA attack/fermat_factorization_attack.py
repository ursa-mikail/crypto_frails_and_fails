"""
The crack relates to Pierre de Fermat’s discovery that we can factorise a modulus into its prime number factors fairly easily — if the prime numbers are fairly close together.
"""
#!pip install gmpy2
import gmpy2
from gmpy2 import mpz, isqrt, is_square
import random

class RSAKey:
    def __init__(self):
        self.e = bytearray(0)
        self.n = bytearray(0)

def FermatFactor(n: int, max_steps: int):
    if n % 2 == 0:
        return 2, n // 2

    a = isqrt(n)
    if a * a < n:
        a += 1

    for _ in range(max_steps):
        b2 = a * a - n
        if is_square(b2):
            b = isqrt(b2)
            return int(a + b), int(a - b)
        a += 1

    return None

# Set key size and steps
nsize = 512
max_steps = 100000  # increased to allow success

print(f"Prime number size: {nsize} bits\n")

# === Try with p and q close to each other (within 2^20) ===
print("== Try with p and q close to each other (within 2^20) ==")
p = gmpy2.next_prime(random.getrandbits(nsize))
q = gmpy2.next_prime(p + random.randint(1, 2**20))  # very close primes

n = int(p * q)
print(f"N = {n}")
result = FermatFactor(n, max_steps)

if result and result[0] * result[1] == n:
    print("[SUCCESS] Fermat was able to factor n.")
    print(f"Factors: p = {result[0]}, q = {result[1]}")
else:
    print("[FAILURE] Fermat failed to factor n.")

# === Try with p and q far apart ===
print("\n== Try with p and q as random primes ==")
p = gmpy2.next_prime(random.getrandbits(nsize))
q = gmpy2.next_prime(random.getrandbits(nsize))  # not close

n = int(p * q)
print(f"N = {n}")
result = FermatFactor(n, max_steps)

if result and result[0] * result[1] == n:
    print("[SUCCESS] Fermat was able to factor n.")
    print(f"Factors: p = {result[0]}, q = {result[1]}")
else:
    print("[FAILURE] Fermat failed to factor n.")

"""
Prime number size: 512 bits

== Try with p and q close to each other (within 2^20) ==
N = 12273822994108615269829516948963013142439559472035528892644412741766067827308128077256866705762223501440668995954090151993490157051131289386327775575402263732241372685877847072870757988906965683541416687453110534720527338138930738425722975801415671704440727935757713933141073726091833937433678648667250045107
[SUCCESS] Fermat was able to factor n.
Factors: p = 3503401631858473526824213000531227186649395529971269053910014848542009467650739055649178871625963191122129992932716652769830919190890697578572858334861491, q = 3503401631858473526824213000531227186649395529971269053910014848542009467650739055649178871625963191122129992932716652769830919190890697578572858334693377

== Try with p and q as random primes ==
N = 45578106397414693662663950072733527270467216393997515475073715202917578907490637642317330074928491071577715891862380395362020010367589188709986841554031514472944422584465271238118297123491251193655256652888969083456729183032412774060773285439893121082610293649727086765015759188077708981429258082158745078553
[FAILURE] Fermat failed to factor n.
"""
