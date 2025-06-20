"""
🧨 Vulnerabilities Illustrated:
Fixed Seed: Makes all PRNG outputs predictable after reset.
Low Entropy or Uninitialized Seed: Makes brute-forcing feasible.
No Entropy Health Check: Could easily use low-quality or reused entropy.
State Recovery: Even if only partial output is leaked, internal state can often be recovered due to LCG reversibility.
"""
from random import randbytes
import time

# Broken PRNG (LCG with known constants and zero seed)
class BrokenLCG:
    def __init__(self, seed=0x00000000):
        self.modulus = 2**32
        self.multiplier = 1664525
        self.increment = 1013904223
        self.state = seed  # Vulnerability: uninitialized or fixed seed

    def next(self):
        self.state = (self.multiplier * self.state + self.increment) % self.modulus
        return self.state

def brute_force_seed(observed_outputs, max_seed=2**24):  # Limit brute-force size for speed
    for possible_seed in range(max_seed):
        test_prng = BrokenLCG(seed=possible_seed)
        test_output = [test_prng.next() for _ in range(len(observed_outputs))]
        if test_output == observed_outputs:
            return possible_seed
    return None

# --- Generate a 4-byte seed ---
time_start = time.time()

num_bytes = 3 # 4
seed_bytes = randbytes(num_bytes)
seed_int = int.from_bytes(seed_bytes, 'big')  # Convert bytes to int

print("Chosen seed:", hex(seed_int))

# Simulate output from victim PRNG
prng = BrokenLCG(seed=seed_int)
observed_outputs = [prng.next() for _ in range(3)]

print("Observed outputs:", observed_outputs)
print("Observed outputs [hex]:", [hex(o) for o in observed_outputs])

# Brute-force to find the seed
recovered_seed = brute_force_seed(observed_outputs, 2**(num_bytes*8))
print("Recovered seed:", hex(recovered_seed) if recovered_seed is not None else "Not found")

time_end = time.time()
time_elapsed = time_end - time_start

print(f'time_elapsed for attack: {time_elapsed} secs')

"""
Chosen seed: 0x825cc3
Observed outputs: [1125014342, 1180531181, 4125594216]
Observed outputs [hex]: ['0x430e5b46', '0x465d79ed', '0xf5e79268']
Recovered seed: 0x825cc3
time_elapsed for attack: 27.516157388687134 secs
"""