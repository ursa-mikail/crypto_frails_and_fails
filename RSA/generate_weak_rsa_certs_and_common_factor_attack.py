# generate_weak_rsa.py
#!pip install pycryptodome
"""
keys/1.pem, keys/2.pem: public keys (with shared p)

messages/1.bin, messages/2.bin: messages encrypted with the corresponding key

(Optional) 1_priv.pem and 2_priv.pem: for validation
"""
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import getPrime
from Crypto.Random import get_random_bytes

def save_public_key(key, path):
    with open(path, 'wb') as f:
        f.write(key.publickey().export_key())

def save_private_key(key, path):
    with open(path, 'wb') as f:
        f.write(key.export_key())

def encrypt_message(pubkey, message):
    cipher = PKCS1_OAEP.new(pubkey)
    return cipher.encrypt(message)

if __name__ == "__main__":
    os.makedirs("keys", exist_ok=True)
    os.makedirs("messages", exist_ok=True)

    e = 65537
    p = getPrime(512)  # shared prime
    q1 = getPrime(512)
    q2 = getPrime(512)

    # RSA key 1: n1 = p * q1
    key1 = RSA.construct((p*q1, e, pow(e, -1, (p-1)*(q1-1)), p, q1))
    save_public_key(key1, "keys/1.pem")
    save_private_key(key1, "keys/1_priv.pem")

    # RSA key 2: n2 = p * q2 (shared p)
    key2 = RSA.construct((p*q2, e, pow(e, -1, (p-1)*(q2-1)), p, q2))
    save_public_key(key2, "keys/2.pem")
    save_private_key(key2, "keys/2_priv.pem")

    # Encrypt messages with public keys
    message1 = b"Secret message for key 1"
    message2 = b"Top secret for key 2"

    ciphertext1 = encrypt_message(key1.publickey(), message1)
    ciphertext2 = encrypt_message(key2.publickey(), message2)

    with open("messages/1.bin", "wb") as f:
        f.write(ciphertext1)

    with open("messages/2.bin", "wb") as f:
        f.write(ciphertext2)

    print("✅ Generated weak keys and encrypted messages.")

"""
✅ Generated weak keys and encrypted messages
"""

""" 
✅ Reads .pem RSA public keys from a folder
✅ Computes pairwise GCD(n1, n2) to detect shared primes
✅ Reconstructs private keys when a shared prime is found
✅ Saves the reconstructed private key to a .pem file


Caveat:
- ZeroDivisionError 
🔓 Shared prime found between 2_priv.pem and 1_priv.pem

That means both n1 and n2 are the same — comparing 2 private keys that were generated with the exact same p and q, so:

GCD(n1, n2) == n1 == n2

Then q = n1 // p becomes q = n1 // n1 == 1

So phi = (p - 1) * (q - 1) becomes phi = (n1 - 1) * 0 = 0

And inverse(e, 0) raises ZeroDivisionError 🚨
"""

import os
from itertools import combinations
from Crypto.PublicKey import RSA
from Crypto.Util.number import GCD, inverse
from pathlib import Path

def extract_moduli_from_pem(folder_path):
    """Extract modulus n from each PEM public key file."""
    moduli = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pem") and "priv" not in filename:
            full_path = os.path.join(folder_path, filename)
            with open(full_path, "rb") as f:
                try:
                    key = RSA.import_key(f.read())
                    moduli[filename] = key.n
                except Exception as e:
                    print(f"❌ Could not parse {filename}: {e}")
    return moduli

def reconstruct_private_key(n, p, e=65537):
    """Reconstruct private RSA key from n and one shared prime p."""
    q = n // p
    if p == q:
        print("❌ p and q are equal! Bad key.")
        return None
    phi = (p - 1) * (q - 1)
    try:
        d = inverse(e, phi)
    except ZeroDivisionError: # ✅ Add a sanity check to skip exact duplicates
        print("❌ Zero division while computing inverse. Invalid key.")
        return None
    try:
        key = RSA.construct((n, e, d, p, q))
        return key
    except Exception as e:
        print(f"❌ Failed to construct private key: {e}")
        return None

def save_private_key(key, output_path):
    with open(output_path, "wb") as f:
        f.write(key.export_key())

def find_shared_primes_and_recover_keys(moduli_dict, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    filenames = list(moduli_dict.keys())
    for f1, f2 in combinations(filenames, 2):
        n1 = moduli_dict[f1]
        n2 = moduli_dict[f2]

        if n1 == n2:
            continue  # skip identical moduli

        p = GCD(n1, n2)
        if p != 1 and p != n1 and p != n2:
            print(f"🔓 Shared prime found between {f1} and {f2}")
            
            priv1 = reconstruct_private_key(n1, p)
            priv2 = reconstruct_private_key(n2, p)
            
            if priv1:
                out1 = os.path.join(output_folder, f1.replace(".pem", "_priv.pem"))
                save_private_key(priv1, out1)
                print(f"✅ Recovered and saved private key: {out1}")
            
            if priv2:
                out2 = os.path.join(output_folder, f2.replace(".pem", "_priv.pem"))
                save_private_key(priv2, out2)
                print(f"✅ Recovered and saved private key: {out2}")

if __name__ == "__main__":
    pem_folder = "keys/"           # folder containing .pem files
    output_priv_folder = "cracked_keys/"  # folder to save recovered keys
    moduli = extract_moduli_from_pem(pem_folder)
    find_shared_primes_and_recover_keys(moduli, output_priv_folder)

"""
🔓 Shared prime found between 1.pem and 2.pem
✅ Recovered and saved private key: cracked_keys/1_priv.pem
✅ Recovered and saved private key: cracked_keys/2_priv.pem

project/
├── keys/
│   ├── 1.pem
│   ├── 2.pem
│   └── ... other public keys ...
├── cracked_keys/
│   ├── 1_priv.pem
│   └── 2_priv.pem
└── crack_shared_prime_rsa.py

"""
