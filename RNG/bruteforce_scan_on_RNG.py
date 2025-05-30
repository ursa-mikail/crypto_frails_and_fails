import time
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

# Simulated Weak PRNG (like C's rand)
def weak_rng_seed(seed):
    random.seed(seed)
    return bytes([random.randint(0, 255) for _ in range(16)])  # 128-bit AES key

# Encrypt with AES-CBC using predictable PRNG key and fixed IV
def encrypt_with_weak_key(seed, plaintext):
    key = weak_rng_seed(seed)
    iv = b'\x00' * 16  # Weak: fixed IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext

# Try to brute-force key by guessing seed
def brute_force_key(ciphertext, known_plaintext_prefix, time_window_start, time_window_end):
    iv = b'\x00' * 16
    for guessed_seed in range(time_window_start, time_window_end):
        key = weak_rng_seed(guessed_seed)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        try:
            decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
            if decrypted.startswith(known_plaintext_prefix):
                return guessed_seed, decrypted
        except:
            continue
    return None, None

# --- Simulate attack ---
# Victim encrypts a message
plaintext = b"Top Secret: Launch Code 1234"
seed_used = int(time.time())  # Seed is current timestamp
ciphertext = encrypt_with_weak_key(seed_used, plaintext)

# Attacker knows it's encrypted recently and message starts with "Top Secret"
guess_window = 60  # seconds
start_time = seed_used - guess_window
end_time = seed_used + 1

print(f"[*] Ciphertext: {ciphertext.hex()}")
print(f"[*] Brute-forcing in time window: {start_time} to {end_time}...")

guessed_seed, recovered = brute_force_key(ciphertext, b"Top Secret", start_time, end_time)

if recovered:
    print(f"[+] Seed found: {guessed_seed}")
    print(f"[+] Recovered plaintext: {recovered}")
else:
    print("[-] Failed to recover plaintext.")

"""
[*] Ciphertext: 9e39720143de7b50a55782972b4bed00ee1bd20fc1bcd46e9ed1eb456a8b5245
[*] Brute-forcing in time window: 1748645386 to 1748645447...
[+] Seed found: 1748645446
[+] Recovered plaintext: b'Top Secret: Launch Code 1234'
"""