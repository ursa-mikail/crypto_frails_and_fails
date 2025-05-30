#!pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import time
from datetime import datetime

BLOCK_SIZE = 16

# Simulated Oracle
class Oracle:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(pad(plaintext, BLOCK_SIZE))

    def decrypt_and_check_padding(self, ciphertext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        try:
            plaintext = cipher.decrypt(ciphertext)
            unpad(plaintext, BLOCK_SIZE)
            return True  # Padding is valid
        except ValueError:
            return False  # Padding is invalid

# Setup
key = get_random_bytes(16)
iv = get_random_bytes(16)
oracle = Oracle(key, iv)
target_plaintext = b"SecretMessage!!!"  # Example plaintext, can be any length
ciphertext = oracle.encrypt(target_plaintext)

# Break into blocks, prepend IV as C0
blocks = [iv] + [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
assert len(blocks) >= 2, "Need at least 2 blocks for POODLE attack"

recovered_plaintext = bytearray()

print(f"\n🔐 Simulating POODLE on AES-CBC (full message):")
overall_start = time.time()
print(f"⏳ Start Time: {datetime.now().isoformat()}\n")

# Attack each ciphertext block pair (C(i-1), C(i)) to recover P(i)
for block_index in range(1, len(blocks)):
    C_prev = blocks[block_index - 1]
    C_curr = blocks[block_index]
    recovered_block = bytearray(BLOCK_SIZE)

    print(f"🔎 Recovering block {block_index}...")

    # Recover bytes from last to first in this block
    for byte_index in reversed(range(BLOCK_SIZE)):
        pad_val = BLOCK_SIZE - byte_index
        prefix = bytearray(os.urandom(byte_index))

        for guess in range(256):
            crafted_block = bytearray(prefix)
            crafted_block.append(guess)
            for k in range(byte_index + 1, BLOCK_SIZE):
                crafted_block.append(C_prev[k] ^ recovered_block[k] ^ pad_val)

            test_cipher = bytes(crafted_block) + C_curr
            if oracle.decrypt_and_check_padding(test_cipher):
                recovered_byte = guess ^ pad_val ^ C_prev[byte_index]
                recovered_block[byte_index] = recovered_byte

                # Show ASCII char or '.' for non-printable
                ascii_char = chr(recovered_byte) if 32 <= recovered_byte < 127 else '.'

                print(f"  🧩 Byte {BLOCK_SIZE - byte_index:2}: {recovered_byte:02x} "
                      f"(ASCII: {ascii_char}) "
                      f"| Time: {datetime.now().isoformat()}")
                print(f"    🔸 Partial block recovered: {recovered_block.hex()} ({recovered_block})")
                break

    recovered_plaintext.extend(recovered_block)

overall_end = time.time()

# Remove padding from recovered plaintext
unpadded_plaintext = unpad(recovered_plaintext, BLOCK_SIZE)

print(f"\n✅ Recovered plaintext (with padding): {recovered_plaintext}")
print(f"✅ Recovered plaintext (unpadded): {unpadded_plaintext}")
print(f"✅ Original target plaintext:     {target_plaintext}")
print(f"⏹️ End Time: {datetime.now().isoformat()}")
print(f"🕒 Total Duration: {overall_end - overall_start:.3f} seconds")

# Assert full recovered plaintext matches original
assert unpadded_plaintext == target_plaintext, "❌ Recovered plaintext does not match target!"

print("\n🎉 Assertion passed: Full recovered plaintext matches the original target plaintext.")

"""
🔐 Simulating POODLE on AES-CBC (full message):
⏳ Start Time: 2025-05-30T21:48:21.320967

🔎 Recovering block 1...
  🧩 Byte  1: 21 (ASCII: !) | Time: 2025-05-30T21:48:21.327191
    🔸 Partial block recovered: 00000000000000000000000000000021 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00!'))
  🧩 Byte  2: 21 (ASCII: !) | Time: 2025-05-30T21:48:21.332505
    🔸 Partial block recovered: 00000000000000000000000000002121 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00!!'))
  🧩 Byte  3: 21 (ASCII: !) | Time: 2025-05-30T21:48:21.350804
    🔸 Partial block recovered: 00000000000000000000000000212121 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00!!!'))
  🧩 Byte  4: 65 (ASCII: e) | Time: 2025-05-30T21:48:21.351748
    🔸 Partial block recovered: 00000000000000000000000065212121 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00e!!!'))
  🧩 Byte  5: 67 (ASCII: g) | Time: 2025-05-30T21:48:21.359518
    🔸 Partial block recovered: 00000000000000000000006765212121 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ge!!!'))
  🧩 Byte  6: 61 (ASCII: a) | Time: 2025-05-30T21:48:21.368591
    🔸 Partial block recovered: 00000000000000000000616765212121 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00age!!!'))
  🧩 Byte  7: 73 (ASCII: s) | Time: 2025-05-30T21:48:21.379148
    🔸 Partial block recovered: 00000000000000000073616765212121 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00sage!!!'))
  🧩 Byte  8: 73 (ASCII: s) | Time: 2025-05-30T21:48:21.379801
    🔸 Partial block recovered: 00000000000000007373616765212121 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00ssage!!!'))
  🧩 Byte  9: 65 (ASCII: e) | Time: 2025-05-30T21:48:21.385204
    🔸 Partial block recovered: 00000000000000657373616765212121 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00essage!!!'))
  🧩 Byte 10: 4d (ASCII: M) | Time: 2025-05-30T21:48:21.394513
    🔸 Partial block recovered: 0000000000004d657373616765212121 (bytearray(b'\x00\x00\x00\x00\x00\x00Message!!!'))
  🧩 Byte 11: 74 (ASCII: t) | Time: 2025-05-30T21:48:21.395613
    🔸 Partial block recovered: 0000000000744d657373616765212121 (bytearray(b'\x00\x00\x00\x00\x00tMessage!!!'))
  🧩 Byte 12: 65 (ASCII: e) | Time: 2025-05-30T21:48:21.403077
    🔸 Partial block recovered: 0000000065744d657373616765212121 (bytearray(b'\x00\x00\x00\x00etMessage!!!'))
  🧩 Byte 13: 72 (ASCII: r) | Time: 2025-05-30T21:48:21.406732
    🔸 Partial block recovered: 0000007265744d657373616765212121 (bytearray(b'\x00\x00\x00retMessage!!!'))
  🧩 Byte 14: 63 (ASCII: c) | Time: 2025-05-30T21:48:21.409612
    🔸 Partial block recovered: 0000637265744d657373616765212121 (bytearray(b'\x00\x00cretMessage!!!'))
  🧩 Byte 15: 65 (ASCII: e) | Time: 2025-05-30T21:48:21.411016
    🔸 Partial block recovered: 0065637265744d657373616765212121 (bytearray(b'\x00ecretMessage!!!'))
  🧩 Byte 16: 53 (ASCII: S) | Time: 2025-05-30T21:48:21.411236
    🔸 Partial block recovered: 5365637265744d657373616765212121 (bytearray(b'SecretMessage!!!'))
🔎 Recovering block 2...
  🧩 Byte  1: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.411512
    🔸 Partial block recovered: 00000000000000000000000000000010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'))
  🧩 Byte  2: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.417065
    🔸 Partial block recovered: 00000000000000000000000000001010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10'))
  🧩 Byte  3: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.419015
    🔸 Partial block recovered: 00000000000000000000000000101010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10'))
  🧩 Byte  4: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.425481
    🔸 Partial block recovered: 00000000000000000000000010101010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\x10'))
  🧩 Byte  5: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.427077
    🔸 Partial block recovered: 00000000000000000000001010101010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\x10\x10'))
  🧩 Byte  6: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.431108
    🔸 Partial block recovered: 00000000000000000000101010101010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\x10\x10\x10'))
  🧩 Byte  7: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.432262
    🔸 Partial block recovered: 00000000000000000010101010101010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte  8: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.433470
    🔸 Partial block recovered: 00000000000000001010101010101010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte  9: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.433868
    🔸 Partial block recovered: 00000000000000101010101010101010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte 10: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.437351
    🔸 Partial block recovered: 00000000000010101010101010101010 (bytearray(b'\x00\x00\x00\x00\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte 11: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.453794
    🔸 Partial block recovered: 00000000001010101010101010101010 (bytearray(b'\x00\x00\x00\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte 12: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.468440
    🔸 Partial block recovered: 00000000101010101010101010101010 (bytearray(b'\x00\x00\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte 13: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.478048
    🔸 Partial block recovered: 00000010101010101010101010101010 (bytearray(b'\x00\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte 14: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.485161
    🔸 Partial block recovered: 00001010101010101010101010101010 (bytearray(b'\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte 15: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.492073
    🔸 Partial block recovered: 00101010101010101010101010101010 (bytearray(b'\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
  🧩 Byte 16: 10 (ASCII: .) | Time: 2025-05-30T21:48:21.497263
    🔸 Partial block recovered: 10101010101010101010101010101010 (bytearray(b'\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))

✅ Recovered plaintext (with padding): bytearray(b'SecretMessage!!!\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10')
✅ Recovered plaintext (unpadded): bytearray(b'SecretMessage!!!')
✅ Original target plaintext:     b'SecretMessage!!!'
⏹️ End Time: 2025-05-30T21:48:21.497852
🕒 Total Duration: 0.177 seconds

🎉 Assertion passed: Full recovered plaintext matches the original target plaintext.
"""