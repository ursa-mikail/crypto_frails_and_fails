#!pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

def aes_gcm_siv_encrypt(key, plaintext, nonce):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext, tag

def aes_gcm_siv_decrypt(key, ciphertext, nonce, tag):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

if __name__ == "__main__":
    key = get_random_bytes(32)
    nonce = os.urandom(12)  # Incorrect randomness generation, should be unique per encryption
    
    plaintext1 = pad(b"Message One", 16)
    plaintext2 = pad(b"Message Two", 16)
    
    # Encrypt with same nonce (vulnerable)
    ciphertext1, tag1 = aes_gcm_siv_encrypt(key, plaintext1, nonce)
    ciphertext2, tag2 = aes_gcm_siv_encrypt(key, plaintext2, nonce)
    
    # With nonce reuse: c1 XOR c2 = p1 XOR p2
    # So if we know p1, we can compute: c1 XOR c2 XOR p1 = p2
    recovered_plaintext2 = bytes([c1 ^ c2 ^ p1 for c1, c2, p1 in zip(ciphertext1, ciphertext2, plaintext1)])
    print(f"Recovered plaintext2: {unpad(recovered_plaintext2, 16)}")


"""
Recovered plaintext2: b'Message Two'
"""

"""
- Real Nonce Reuse Vulnerability:
XOR relationship: c1 ⊕ c2 = p1 ⊕ p2
Known plaintext attack allows recovery of other plaintexts

- Authentication Still Works:
Even with nonce reuse, GCM still detects tampering
The vulnerability is information leakage, not forgery

- Correct Usage:
Always use unique nonces
Let the library generate nonces automatically when possible

1. Complete Plaintext Recovery: When nonce is reused and plaintexts are same length

2. Partial Recovery: When only part of the plaintext structure is known

3. Limited Recovery: With different length plaintexts, only overlapping parts can be recovered

4. Security with Unique Nonces: The vulnerability disappears with proper nonce usage
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def demonstrate_nonce_reuse_vulnerability():
    """Demonstrate the real nonce reuse vulnerability in AES-GCM"""
    print("="*60)
    print("REAL NONCE REUSE VULNERABILITY DEMONSTRATION")
    print("="*60)
    
    # Fixed key and NONCE (this is the vulnerability - reusing nonce)
    key = get_random_bytes(32)
    nonce = b"fixed_nonce_12"  # This is reused - VULNERABLE!
    
    # Two different plaintexts - using same length
    plaintext1 = b"Secret message one!!"  # 20 bytes
    plaintext2 = b"Secret message two!!"  # 20 bytes
    
    print(f"Original plaintext 1: {plaintext1}")
    print(f"Original plaintext 2: {plaintext2}")
    
    # Encrypt both with same nonce (VULNERABLE)
    cipher1 = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext1, tag1 = cipher1.encrypt_and_digest(plaintext1)
    
    cipher2 = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext2, tag2 = cipher2.encrypt_and_digest(plaintext2)
    
    # ====== ATTACK ======
    # When nonce is reused, the keystream is the same
    # So: ciphertext1 = plaintext1 ⊕ keystream
    #     ciphertext2 = plaintext2 ⊕ keystream
    # Therefore: ciphertext1 ⊕ ciphertext2 = plaintext1 ⊕ plaintext2
    
    xor_ciphertexts = bytes(a ^ b for a, b in zip(ciphertext1, ciphertext2))
    xor_plaintexts = bytes(a ^ b for a, b in zip(plaintext1, plaintext2))
    
    print(f"\nXOR of ciphertexts equals XOR of plaintexts: {xor_ciphertexts == xor_plaintexts}")
    
    # If attacker knows 1 plaintext, they can recover the other
    print("\n=== KNOWN PLAINTEXT ATTACK ===")
    # Suppose attacker knows plaintext1 (common in real scenarios)
    recovered_plaintext2 = bytes(a ^ b ^ c for a, b, c in zip(ciphertext1, ciphertext2, plaintext1))
    print(f"Recovered plaintext 2: {recovered_plaintext2}")
    print(f"Recovery successful: {recovered_plaintext2 == plaintext2}")
    
    # Or if they know plaintext2, they can recover plaintext1
    recovered_plaintext1 = bytes(a ^ b ^ c for a, b, c in zip(ciphertext1, ciphertext2, plaintext2))
    print(f"Recovered plaintext 1: {recovered_plaintext1}")
    print(f"Recovery successful: {recovered_plaintext1 == plaintext1}")

def demonstrate_advanced_attack():
    """Show practical attack scenario with structured data"""
    print("\n" + "="*60)
    print("PRACTICAL ATTACK SCENARIO")
    print("="*60)
    
    key = get_random_bytes(32)
    nonce = b"reused_nonce!!"  # Reused - VULNERABLE!
    
    # Real-world scenario: attacker knows some structure - SAME LENGTH
    known_plaintext = b"GET /index.html HTTP/1"  # 22 bytes
    unknown_plaintext = b"GET /secret_data HTTP/1"  # 22 bytes
    
    print(f"Known plaintext:    {known_plaintext}")
    print(f"Unknown plaintext:  {unknown_plaintext}")
    
    # Encrypt both with same nonce
    cipher1 = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext1, tag1 = cipher1.encrypt_and_digest(known_plaintext)
    
    cipher2 = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext2, tag2 = cipher2.encrypt_and_digest(unknown_plaintext)
    
    # Attack: Recover unknown plaintext using known plaintext
    recovered_secret = bytes(a ^ b ^ c for a, b, c in zip(ciphertext1, ciphertext2, known_plaintext))
    
    print(f"\nRecovered plaintext: {recovered_secret}")
    print(f"Recovery successful: {recovered_secret == unknown_plaintext}")
    
    # Show the XOR relationship
    print(f"\nXOR relationship holds: {bytes(a^b for a,b in zip(ciphertext1, ciphertext2)) == bytes(a^b for a,b in zip(known_plaintext, unknown_plaintext))}")

def demonstrate_partial_knowledge_attack():
    """Show attack when only part of plaintext is known"""
    print("\n" + "="*60)
    print("PARTIAL KNOWLEDGE ATTACK")
    print("="*60)
    
    key = get_random_bytes(32)
    nonce = b"partial_attack!!"
    
    # Scenario: attacker knows part of the message format - SAME LENGTH
    secret1 = b"Password: MySecret123!!"  # 23 bytes
    secret2 = b"Password: AdminPass456!!"  # 23 bytes
    known_part = b"Password: "  # Attacker knows this prefix (10 bytes)
    
    print(f"Secret 1:     {secret1}")
    print(f"Secret 2:     {secret2}")
    print(f"Known prefix: {known_part}")
    
    cipher1 = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext1, tag1 = cipher1.encrypt_and_dest(secret1)
    
    cipher2 = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext2, tag2 = cipher2.encrypt_and_digest(secret2)
    
    # Attack: Recover unknown parts using known prefix
    recovered_secret2 = bytearray()
    
    for i in range(len(secret2)):
        if i < len(known_part):
            # Use known byte
            recovered_secret2.append(known_part[i])
        else:
            # Recover unknown byte using XOR relationship
            recovered_byte = ciphertext1[i] ^ ciphertext2[i] ^ secret1[i]
            recovered_secret2.append(recovered_byte)
    
    print(f"Recovered secret2: {bytes(recovered_secret2)}")
    print(f"Recovery successful: {bytes(recovered_secret2) == secret2}")

def demonstrate_different_length_attack():
    """Show how to handle different length plaintexts"""
    print("\n" + "="*60)
    print("DIFFERENT LENGTH ATTACK")
    print("="*60)
    
    key = get_random_bytes(32)
    nonce = b"diff_length_att"
    
    # Different length plaintexts
    short_plaintext = b"Short message"  # 13 bytes
    long_plaintext = b"This is a much longer secret message"  # 36 bytes
    
    print(f"Short plaintext: {short_plaintext}")
    print(f"Long plaintext:  {long_plaintext}")
    
    cipher1 = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext1, tag1 = cipher1.encrypt_and_digest(short_plaintext)
    
    cipher2 = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext2, tag2 = cipher2.encrypt_and_digest(long_plaintext)
    
    # Attack: Can only recover overlapping parts
    min_length = min(len(short_plaintext), len(long_plaintext))
    
    print(f"\nCan recover first {min_length} bytes of longer message:")
    recovered_part = bytes(ciphertext1[i] ^ ciphertext2[i] ^ short_plaintext[i] for i in range(min_length))
    print(f"Recovered part: {recovered_part}")
    print(f"Actual start:   {long_plaintext[:min_length]}")
    print(f"Partial recovery successful: {recovered_part == long_plaintext[:min_length]}")

def correct_usage():
    """Show the CORRECT way to use AES-GCM"""
    print("\n" + "="*60)
    print("CORRECT USAGE - UNIQUE NONCE EVERY TIME")
    print("="*60)
    
    key = get_random_bytes(32)
    
    plaintext1 = b"Message one"
    plaintext2 = b"Message two"
    
    # CORRECT: Generate unique nonce for each encryption
    cipher1 = AES.new(key, AES.MODE_GCM)
    ciphertext1, tag1 = cipher1.encrypt_and_digest(plaintext1)
    
    cipher2 = AES.new(key, AES.MODE_GCM)  # Auto-generates unique nonce
    ciphertext2, tag2 = cipher2.encrypt_and_digest(plaintext2)
    
    print("With unique nonces:")
    print(f"Nonce 1: {cipher1.nonce.hex()}")
    print(f"Nonce 2: {cipher2.nonce.hex()}")
    print("Nonces are different - SECURE!")
    
    # Verify the XOR relationship doesn't hold with proper usage
    min_len = min(len(ciphertext1), len(ciphertext2))
    xor_ciphertexts = bytes(ciphertext1[i] ^ ciphertext2[i] for i in range(min_len))
    xor_plaintexts = bytes(plaintext1[i] ^ plaintext2[i] for i in range(min_len))
    print(f"XOR relationship holds (should be False): {xor_ciphertexts == xor_plaintexts}")

if __name__ == "__main__":
    demonstrate_nonce_reuse_vulnerability()
    demonstrate_advanced_attack()
    demonstrate_different_length_attack()
    correct_usage()

"""
============================================================
REAL NONCE REUSE VULNERABILITY DEMONSTRATION
============================================================
Original plaintext 1: b'Secret message one!!'
Original plaintext 2: b'Secret message two!!'

XOR of ciphertexts equals XOR of plaintexts: True

=== KNOWN PLAINTEXT ATTACK ===
Recovered plaintext 2: b'Secret message two!!'
Recovery successful: True
Recovered plaintext 1: b'Secret message one!!'
Recovery successful: True

============================================================
PRACTICAL ATTACK SCENARIO
============================================================
Known plaintext:    b'GET /index.html HTTP/1'
Unknown plaintext:  b'GET /secret_data HTTP/1'

Recovered plaintext: b'GET /secret_data HTTP/'
Recovery successful: False

XOR relationship holds: True

============================================================
DIFFERENT LENGTH ATTACK
============================================================
Short plaintext: b'Short message'
Long plaintext:  b'This is a much longer secret message'

Can recover first 13 bytes of longer message:
Recovered part: b'This is a muc'
Actual start:   b'This is a muc'
Partial recovery successful: True

============================================================
CORRECT USAGE - UNIQUE NONCE EVERY TIME
============================================================
With unique nonces:
Nonce 1: be122e0b11b47a58c59b2e7eb147ab5d
Nonce 2: 684873b3c1891a69660690ac7e0b6b15
Nonces are different - SECURE!
XOR relationship holds (should be False): False
"""    