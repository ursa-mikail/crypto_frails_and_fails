from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def aes_ctr_encrypt(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
    return cipher.encrypt(plaintext)

def aes_gcm_encrypt(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext, tag

def ascii_print(bs: bytes) -> str:
    return ''.join(chr(b) if 32 <= b <= 126 else '.' for b in bs)

def demo_recovery():
    key = get_random_bytes(16)
    iv = get_random_bytes(8)

    p1 = b"Attack at dawn!"
    p2 = b"Retreat at night time!"

    print("CTR Mode:")
    # Encrypt with reused nonce (CTR)
    c1 = aes_ctr_encrypt(key, iv, p1)
    c2 = aes_ctr_encrypt(key, iv, p2)

    # XOR ciphertexts -> XOR plaintexts
    xor_plaintexts = xor_bytes(c1, c2)

    print("XOR of plaintexts (bytes):", xor_plaintexts)
    print("XOR of plaintexts (ASCII):", ascii_print(xor_plaintexts))
    print()

    # Assume attacker guesses part of p1 (e.g. "Attack at ")
    guess_p1 = p1[:12] # b"Attack at "
    # guess_p1 = p1
    recovered_p2_part = xor_bytes(xor_plaintexts[:len(guess_p1)], guess_p1)
    print(f"Guessed p1 part: {guess_p1.decode()}")
    print(f"Recovered p2 part: {recovered_p2_part.decode(errors='replace')}")
    print()

    print("GCM Mode:")
    # Encrypt with reused nonce (GCM)
    c1, t1 = aes_gcm_encrypt(key, iv, p1)
    c2, t2 = aes_gcm_encrypt(key, iv, p2)

    # XOR ciphertexts -> XOR plaintexts
    xor_plaintexts = xor_bytes(c1, c2)
    
    print("XOR of plaintexts (bytes):", xor_plaintexts)
    print("XOR of plaintexts (ASCII):", ascii_print(xor_plaintexts))
    print()

    # Assume attacker guesses part of p1 (e.g. "Attack at ")
    guess_p1 = b"Attack at "
    recovered_p2_part = xor_bytes(xor_plaintexts[:len(guess_p1)], guess_p1)
    print(f"Guessed p1 part: {guess_p1.decode()}")
    print(f"Recovered p2 part: {recovered_p2_part.decode(errors='replace')}")
    print()   

if __name__ == "__main__":
    demo_recovery()

"""
CTR Mode:
XOR of plaintexts (bytes): b'\x13\x11\x00\x13\x06\nTA\x15TD\x0f\x1e\tI'
XOR of plaintexts (ASCII): ......TA.TD...I

Guessed p1 part: Attack at da
Recovered p2 part: Retreat at n

GCM Mode:
XOR of plaintexts (bytes): b'\x13\x11\x00\x13\x06\nTA\x15TD\x0f\x1e\tI'
XOR of plaintexts (ASCII): ......TA.TD...I

Guessed p1 part: Attack at 
Recovered p2 part: Retreat at
"""