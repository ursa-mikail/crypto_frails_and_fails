from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Encrypt message using AES-CBC without HMAC
def encrypt_aes_cbc_no_auth(key, plaintext):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return iv + ciphertext  # Prepend IV

# Decrypt message without checking integrity
def decrypt_aes_cbc_no_auth(key, iv_ciphertext):
    iv = iv_ciphertext[:16]
    ciphertext = iv_ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext
    except ValueError:
        return b"[!] Padding error detected"

# Simulate attacker flipping 1 bit in ciphertext
def tamper(ciphertext, byte_index):
    tampered = bytearray(ciphertext)
    tampered[byte_index] ^= 0x01  # Flip 1 bit
    return bytes(tampered)

# --- Setup ---
key = os.urandom(16)
plaintext = b"USER=admin;ACCESS=NO;"
print("[*] Original plaintext:", plaintext)

# Case: [Detected]
# Step 1: Encrypt
iv_cipher = encrypt_aes_cbc_no_auth(key, plaintext)
print("[*] Encrypted (IV + ciphertext):", iv_cipher.hex())

# Step 3: Decrypt tampered message
decrypted = decrypt_aes_cbc_no_auth(key, iv_cipher)
print("[*] Decrypted (no tampering):", decrypted)

# Step 2: Tamper with ciphertext
tampered_cipher = tamper(iv_cipher, 25)  # Flip a bit in the ciphertext
print("[*] Tampered ciphertext:", tampered_cipher.hex())

# Step 3: Decrypt tampered message
decrypted = decrypt_aes_cbc_no_auth(key, tampered_cipher)
print("[*] Decrypted (after tampering):", decrypted)

# Case: [Un-Detected]
#plaintext = b"USER=admin;ACCESS=NO;PADPAD"  # Add dummy padding to make it cleanly 2+ blocks

print("[*] Original plaintext:", plaintext)

# Step 1: Encrypt
iv_cipher = encrypt_aes_cbc_no_auth(key, plaintext)
print("[*] Encrypted (IV + ciphertext):", iv_cipher.hex())

# Step 2: Tamper with ciphertext (middle block, not last block)
tampered_cipher = tamper(iv_cipher, 20)  # Flip bit in second block (not IV, not final block)
print("[*] Tampered ciphertext:", tampered_cipher.hex())

# Step 3: Decrypt tampered message
decrypted = decrypt_aes_cbc_no_auth(key, tampered_cipher)
print("[*] Decrypted (after tampering):", decrypted)

"""

AES-CBC decrypts block B_n as:
P_n = AES_DECRYPT(C_n) ⊕ C_{n-1}

So if you flip a bit in C_{n-1}, you affect P_n, even if all padding in P_k is valid.

This lets attackers silently alter decrypted messages.

✅ Real-World Implications
Without HMAC or AES-GCM:

Encrypted cookies can be tampered (flip role=user → role=admin)

Login tokens can be corrupted silently

Software decrypts wrong data and acts on it without knowing

[*] Original plaintext: b'USER=admin;ACCESS=NO;'
[*] Encrypted (IV + ciphertext): e587f64216d99dd5587040c88d33d4905ad96cb2f8a9088f3c9d4422a32647696a4dfd6bdd13e5fb185885404110861f
[*] Decrypted (no tampering): b'USER=admin;ACCESS=NO;'
[*] Tampered ciphertext: e587f64216d99dd5587040c88d33d4905ad96cb2f8a9088f3c9c4422a32647696a4dfd6bdd13e5fb185885404110861f
[*] Decrypted (after tampering): b'[!] Padding error detected'
[*] Original plaintext: b'USER=admin;ACCESS=NO;'
[*] Encrypted (IV + ciphertext): 6f99c9e9207f5d45dff4d01646d8343e65772607129e7a199195c7301f4770395c46e48208fecbe7e5d57e8851ef3503
[*] Tampered ciphertext: 6f99c9e9207f5d45dff4d01646d8343e65772607139e7a199195c7301f4770395c46e48208fecbe7e5d57e8851ef3503
[*] Decrypted (after tampering): b'\xdf\xc5\x043_,\xddT\xffP\xb7]\xc0<c\nS=NO:'


"""


"""
🧨 Goal: Change "NO;" → "YES;" in decrypted plaintext
By tampering with the ciphertext only, while:

Not triggering a padding error

"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Step 1: AES CBC encryption/decryption
def encrypt(key, plaintext):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(plaintext, 16))

def decrypt(key, iv_ciphertext):
    iv = iv_ciphertext[:16]
    ct = iv_ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        return unpad(cipher.decrypt(ct), 16)
    except ValueError:
        return b"[!] Padding error detected"

# Step 2: Bitflipping utility
def flip(c, o, d):
    return c ^ o ^ d

# Step 3: Craft a message with "NO;" starting at block 2 offset 0
key = os.urandom(16)
plaintext = b'USER=admin123456' + b'ACCESS=NO;PAD!!'  # block 1 + block 2
print("[*] Original plaintext:", plaintext)

iv_ciphertext = encrypt(key, plaintext)
print("[*] Encrypted (IV + ciphertext):", iv_ciphertext.hex())

# Step 4: Bitflip "NO;" → "YES" in block 2
ciphertext = bytearray(iv_ciphertext)
# We will change block 1, bytes 8–10 to affect block 2, bytes 8–10
block1_offset = 16
offset_in_block = 7  # "NO;" is at block2[7], i.e., modify block1[7]

# Extract the original plaintext chunk (for clarity)
orig = b'NO;'
target = b'YES'

# Apply the bitflips to block1
for i in range(3):
    index = 16 + 7 + i  # 16 = IV, modify bytes 23–25
    ciphertext[index] ^= orig[i] ^ target[i]

# Step 5: Decrypt modified ciphertext
result = decrypt(key, bytes(ciphertext))
print("[*] Decrypted (after bitflip):", result)


"""
[*] Original plaintext: b'USER=admin123456ACCESS=NO;PAD!!'
[*] Encrypted (IV + ciphertext): 21c70fd23b772a5d371fe535d29e944673adda90c72d9bb8e5e67f8e7861d821c1da6f6944104aabac6696a93e1e51b4
[*] Decrypted (after bitflip): b'\x9a2\x00\x98\xae\xba\x82~\xa1|\xc0\xc1o\xb5B\xf8ACCESS=YESPAD!!'

That output confirms the tampering — the "ACCESS=NO;" turned into "ACCESS=YES" in the decrypted plaintext, but the prefix bytes got corrupted and look like gibberish (because we flipped part of the previous block’s ciphertext). This is expected: CBC bit flipping flips bytes in the previous ciphertext block, so the decrypted block changes only in the targeted bytes, but the previous block’s plaintext decrypts to garbage.

CBC decryption:

P_i = AES_DECRYPT(C_i) XOR C_(i-1)

By flipping bits in C_(i-1), you can control the XOR part and flip plaintext bytes in P_i.

But P_(i-1) depends on C_(i-2) and so on, so the previous block’s plaintext becomes corrupted and looks like random bytes.

1. The target block (ACCESS=NO;PAD!!) was successfully altered from "NO;" → "YES".

2. The previous block (USER=admin123456) became corrupted — you get gibberish, which is fine if you don’t care about that part or it’s not security-critical.

3. This illustrates how lack of authentication enables undetected tampering in CBC mode.


Next:
One byte flip → one byte changed in decrypted plaintext block.
Previous block is untouched if only one byte flipped.
Minimal damage, precise tampering.


def encrypt(key, plaintext):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(plaintext, 16))

def decrypt(key, iv_ciphertext):
    iv = iv_ciphertext[:16]
    ct = iv_ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        return unpad(cipher.decrypt(ct), 16)
    except ValueError:
        return b"[!] Padding error detected"

key = os.urandom(16)
plaintext = b'USER=admin123456ACCESS=NO;PAD!!'
print("[*] Original plaintext:", plaintext)

iv_ciphertext = encrypt(key, plaintext)
print("[*] Encrypted (IV + ciphertext):", iv_ciphertext.hex())

# Target block: 'ACCESS=NO;PAD!!' starts at block 2 (offset 16)
# 'NO;' is at offset 7 in block 2 (byte 23 in ciphertext)
# To flip first byte 'N' (ord('N')=78) to 'Y' (ord('Y')=89),
# flip ciphertext block 1 at byte 23 (16 + 7 = 23)

ciphertext = bytearray(iv_ciphertext)

index_to_flip = 16 + 7  # block 1 offset 7
orig_byte = ord('N')
target_byte = ord('Y')

ciphertext[index_to_flip] ^= orig_byte ^ target_byte

decrypted = decrypt(key, bytes(ciphertext))
print("[*] Decrypted (after 1-byte flip):", decrypted)


"""

