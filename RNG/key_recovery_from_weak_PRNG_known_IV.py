"""
🧠 Attack Summary
A system uses rand() (weak PRNG) to generate both the AES key and IV.

Attacker knows the IV (it’s sent with the ciphertext) and some structure of the plaintext (like b"LOGIN=").

Brute-force the PRNG seed to recreate both the IV and key, verifying the correct one by decrypting the ciphertext and checking the prefix.
"""
import random
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Simulated weak PRNG (like C's rand()) to generate key and IV
def weak_rand_bytes(seed, length):
    random.seed(seed)
    return bytes([random.randint(0, 255) for _ in range(length)])

def generate_key_iv(seed):
    random.seed(seed)
    key = bytes([random.randint(0, 255) for _ in range(16)])
    iv = bytes([random.randint(0, 255) for _ in range(16)])
    return key, iv

# Encrypt using AES-CBC with key and IV from weak PRNG
def encrypt_weak(plaintext, seed):
    key, iv = generate_key_iv(seed)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext, iv

# Brute-force the PRNG seed to match known IV and decrypt
def brute_force_seed(ciphertext, known_iv, known_prefix, time_range):
    print(f"[*] Brute-forcing seeds from {time_range[0]} to {time_range[1]}")
    for guessed_seed in range(time_range[0], time_range[1]):
        key, iv = generate_key_iv(guessed_seed)
        if iv == known_iv:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            try:
                decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
                if decrypted.startswith(known_prefix):
                    return guessed_seed, decrypted
            except:
                continue
    return None, None


# Step 1: Encrypt the message
plaintext = b"LOGIN=admin&pwd=hunter2"
seed = int(time.time())
ciphertext, iv = encrypt_weak(plaintext, seed)

print("[*] Ciphertext:", ciphertext.hex())
print("[*] Known IV:  ", iv.hex())

# Step 2: Brute-force seed using known IV and known prefix
time_window = 60  # seconds
start_time = seed - time_window
end_time = seed + 1

guessed_seed, recovered = brute_force_seed(ciphertext, iv, b"LOGIN=", (start_time, end_time))

if recovered:
    print(f"[+] Success! Seed = {guessed_seed}")
    print(f"[+] Decrypted message: {recovered}")
else:
    print("[-] Failed to recover plaintext.")


"""
[*] Ciphertext: 5d60b95d67c218f15edbd4aebd7c157cc7033dc5a3ccf7a9abd8eba97d8d1c8c
[*] Known IV:   0171422906c892da6e86232c6249c8f6
[*] Brute-forcing seeds from 1748645678 to 1748645739
[+] Success! Seed = 1748645738
[+] Decrypted message: b'LOGIN=admin&pwd=hunter2'

🔐 Why This Is Dangerous
Many devices and libraries have used predictable seeds like time(NULL), PIDs, or MAC addresses.

The IV is often sent in plaintext, so if the attacker sees it and knows the plaintext structure, the seed is practically leaked.

Once the seed is recovered, the full AES key is exposed.

🔒 Real-World Lessons
Always use secrets.token_bytes() or os.urandom() for secure key/IV generation.

Never use predictable sources (time, PID, etc.) as RNG seeds.

CBC is malleable — combining that with weak RNGs opens the door to full plaintext/key recovery.
""""