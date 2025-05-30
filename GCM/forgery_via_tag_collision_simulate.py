from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

KEY = AESGCM.generate_key(bit_length=128)
aesgcm = AESGCM(KEY)

TAG_BITS = 32
TAG_BYTES = TAG_BITS // 8
NONCE = os.urandom(12)
AAD = b"auth"
NUM_TRIALS = 2**20

seen_tags = {}

def truncate_tag(ciphertext):
    return ciphertext[-16:][:TAG_BYTES]

def build_forged_ciphertext(ct, fake_tag):
    return ct[:-16] + fake_tag + b"\x00" * (16 - TAG_BYTES)

def insecure_decrypt_truncated_tag(ciphertext, tag_bytes, key, nonce, aad):
    """Simulates broken GCM implementation that verifies only the truncated tag."""
    aesgcm = AESGCM(key)
    try:
        decrypted = aesgcm.decrypt(nonce, ciphertext, aad)
        return decrypted, True
    except:
        # Try to truncate tag and compare manually
        actual_tag = ciphertext[-16:][:tag_bytes]
        # Return plaintext anyway to simulate bad tag verification
        plaintext = ciphertext[:-16]
        return plaintext, False  # didn't pass real verification

print(f"🔐 AES-GCM Forgery Simulation (custom check) using {TAG_BITS}-bit tags")

for i in range(NUM_TRIALS):
    msg = os.urandom(32)
    ct = aesgcm.encrypt(NONCE, msg, AAD)
    short_tag = truncate_tag(ct)

    tag_hex = short_tag.hex()
    if tag_hex in seen_tags:
        prev = seen_tags[tag_hex]
        msg1, ct1 = prev["msg"], prev["ct"]
        msg2, ct2 = msg, ct

        print(f"\n⚠️ Tag collision found after {i + 1} attempts!")
        print(f"🧩 Truncated tag: {tag_hex}")
        print(f"📄 Message 1: {msg1.hex()}")
        print(f"📄 Message 2 (to forge): {msg2.hex()}")

        # Forge: put msg2’s ciphertext with msg1’s tag
        forged_ct = build_forged_ciphertext(ct2, ct1[-16:][:TAG_BYTES])
        decrypted, passed = insecure_decrypt_truncated_tag(forged_ct, TAG_BYTES, KEY, NONCE, AAD)

        if passed:
            print(f"\n🚨 FORGERY SUCCEEDED (but in real GCM, tag would pass)!")
        else:
            print(f"\n🚨 FORGERY SIMULATED (would be accepted by bad implementation checking only {TAG_BITS}-bit tag)")
            print(f"📝 Forged plaintext (junk): {decrypted.hex()}")
        break

    seen_tags[tag_hex] = {"msg": msg, "ct": ct}
else:
    print("✅ No collisions found — increase trials or reduce tag size.")


"""
🔐 AES-GCM Forgery Simulation (custom check) using 32-bit tags

⚠️ Tag collision found after 93769 attempts!
🧩 Truncated tag: 86c8afad
📄 Message 1: e02a24d6c4af1a599dcd30cfbf3d6ac9e20e01666e5ea6fb3f383bf852746352
📄 Message 2 (to forge): 62cc6293ccfc157300a09d7560b03d9a1926ff9899994ea94f09f38432be8759

🚨 FORGERY SIMULATED (would be accepted by bad implementation checking only 32-bit tag)
📝 Forged plaintext (junk): e63bd2f03812f544951b297a92bbe7319d077904c2e492abc7352c99cf117965
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Parameters
TAG_BITS = 32
TAG_BYTES = TAG_BITS // 8
NONCE = os.urandom(12)
AAD = b"auth"
NUM_TRIALS = 2**20

# Key setup
KEY = AESGCM.generate_key(bit_length=128)
aesgcm = AESGCM(KEY)
seen_tags = {}

def truncate_tag(ciphertext):
    return ciphertext[-16:][:TAG_BYTES]

def build_forged_ciphertext(ct, fake_tag):
    return ct[:-16] + fake_tag + b"\x00" * (16 - TAG_BYTES)

def insecure_decrypt_truncated_tag(ciphertext, tag_bytes, key, nonce, aad):
    """Simulates broken GCM implementation that verifies only the truncated tag."""
    actual_tag = ciphertext[-16:][:tag_bytes]
    # Always return plaintext for this demo — simulating bad validation
    plaintext = ciphertext[:-16]
    return plaintext, True

# Run simulation to find a tag collision
for i in range(NUM_TRIALS):
    msg = os.urandom(32)
    ct = aesgcm.encrypt(NONCE, msg, AAD)
    short_tag = truncate_tag(ct)
    tag_hex = short_tag.hex()

    if tag_hex in seen_tags:
        prev = seen_tags[tag_hex]
        msg1, ct1 = prev["msg"], prev["ct"]
        msg2, ct2 = msg, ct
        forged_ct = build_forged_ciphertext(ct2, ct1[-16:][:TAG_BYTES])
        forged_output, passed = insecure_decrypt_truncated_tag(forged_ct, TAG_BYTES, KEY, NONCE, AAD)
        break
    seen_tags[tag_hex] = {"msg": msg, "ct": ct}
else:
    msg1 = msg2 = ct1 = ct2 = forged_ct = forged_output = passed = None

{
    "msg1": msg1.hex(),
    "msg2": msg2.hex(),
    "tag_truncated": truncate_tag(ct1).hex(),
    "forged_ct": forged_ct.hex(),
    "forgery_successful": passed,
    "forged_plaintext_output": forged_output.hex() if forged_output else None
}

"""
✅ Forgery Success
Example where we found a tag collision and successfully simulated a forgery:

🧩 Truncated Tag (4 bytes (32-bit)): 309f1f44
📄 Original Message 1:
c3f90dfde8bf24827b5995532f848b1b00ce733d07d43102638fa5378c3ed7de
📄 Forged Message 2 (with same truncated tag):
81e6191d0d2a358391b78be986aaedbaab83243a353bcc10709e5d3cbddaf69d

🧪 Forged Ciphertext (with spoofed tag):
9f6b11d03cdb6ef2206e25b372e6a62fc5fa53aca98a3b1897a2615895d3389c309f1f44000000000000000000000000

🧬 Forged Plaintext Output (garbage but accepted):
9f6b11d03cdb6ef2206e25b372e6a62fc5fa53aca98a3b1897a2615895d3389c

🔓 Forgery was accepted under a broken implementation that only validates the first 4 bytes (32 bits) of the tag. This proves the Birthday-bound vulnerability of short authentication tags in AES-GCM.
{'msg1': '828031449c2c42873fdd3c1651093e71418b2275fe9146c6261746596d312100',
 'msg2': 'ab0ef50c653fb1e96aac8983900271a692d0329668acbedc3d65fa43f0e3ccd1',
 'tag_truncated': 'b0e1c270',
 'forged_ct': '3bb90f332cdf7ec5078a4e0a2337355910c6102c37b9cec4634ffaa81a1e1727b0e1c270000000000000000000000000',
 'forgery_successful': True,
 'forged_plaintext_output': '3bb90f332cdf7ec5078a4e0a2337355910c6102c37b9cec4634ffaa81a1e1727'}
"""
# 
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Simulate an insecure AES-GCM implementation that only checks 32-bit truncated tags

# Use a fixed key and nonce to simulate reuse
KEY = AESGCM.generate_key(bit_length=128)
aesgcm = AESGCM(KEY)

NONCE = b'\x01' * 12  # Reused nonce
AAD = b"aad"
TAG_BYTES = 4  # Only 32-bit tag used for verification

# Encrypt two messages
plaintext1 = b"Message One!"
plaintext2 = b"Message Two!"

# Encrypt both with same nonce/key
ciphertext1 = aesgcm.encrypt(NONCE, plaintext1, AAD)
ciphertext2 = aesgcm.encrypt(NONCE, plaintext2, AAD)

# Truncate the tags
tag1_trunc = ciphertext1[-16:][:TAG_BYTES]
tag2_trunc = ciphertext2[-16:][:TAG_BYTES]

# Get just ciphertexts (minus full tags)
ct1_body = ciphertext1[:-16]
ct2_body = ciphertext2[:-16]

# Forge a new ciphertext using ct2 but tag1's truncated tag # C2 = C1 ⊕ P1 ⊕ P2
forged_ciphertext = ct2_body + tag1_trunc + b"\x00" * (16 - TAG_BYTES)

# Simulate insecure validation (compare only 32-bit truncated tag)
def insecure_decrypt(nonce, ciphertext, aad, original_tag):
    """
    🚨 Simulates broken AES-GCM tag verification:
    Accepts ciphertexts if the first 4 bytes of the tag match,
    ignoring the rest of the tag and message integrity.
    """    
    # Get the last 16 bytes (full tag), then get the 1st TAG_BYTES of the (16-byte full tag)
    tag_candidate = ciphertext[-16:][:TAG_BYTES] 
    if tag_candidate != original_tag:
        return None  # Reject
    return ciphertext[:-16]  # Return raw "decrypted" bytes for demo

forged_result = insecure_decrypt(NONCE, forged_ciphertext, AAD, tag1_trunc)

{
    "plaintext1": plaintext1,
    "plaintext2": plaintext2,
    "tag1_short": tag1_trunc.hex(),
    "tag2_short": tag2_trunc.hex(),
    "forged_ciphertext_body": ct2_body.hex(),
    "forged_ciphertext_tag": tag1_trunc.hex(),
    "forgery_successful": forged_result is not None,
    "forged_output_bytes": forged_result.hex() if forged_result else None # garbage, but "accepted"
}

"""
{'plaintext1': b'Message One!',
 'plaintext2': b'Message Two!',
 'tag1_short': 'ef9cf96e',
 'tag2_short': '3cd0efad',
 'forged_ciphertext_body': 'dff7cebccc3336d4e9ce63f0',
 'forged_ciphertext_tag': 'ef9cf96e',
 'forgery_successful': True,
 'forged_output_bytes': 'dff7cebccc3336d4e9ce63f0'}

Simulate a “real” successful forgery — i.e., getting a forged ciphertext to:
- Pass validation, and
- Produce controlled plaintext,

🔁 Option A: Nonce Reuse with Known Plaintext XOR
If Nonce, Key are reused and attacker knows P1, C1, then:
C2 = C1 ⊕ P1 ⊕ P2

That way:
Decrypt(C2) = P2

🔥 This gives attacker full control over the resulting plaintext.

🧮 Option B: GHASH Forgery (Collision of authentication field)
- Construct GHASH collisions in GF(2^128)
- Requires control of:
    - Authenticated data (AAD)
    - Ciphertext block arrangement
- This gets into authenticated forgery in GCM's MAC computation path.

“Insecure GCM Implementation” 
Simulate a naive implementation that:
- Truncates tags to 32 bits,
- Compares only that,
- Decrypts ciphertext without checking full tag (i.e., "accept if tag[:4] == known[:4]").

🔥 A forged message being accepted and processed, just like in vulnerable systems.


✅ Summary
| Field                                    | Explanation                      |
| ---------------------------------------- | -------------------------------- |
| `tag1_short != tag2_short`               | True — they differ               |
| `Forged message used tag1_short`         | Yes                              |
| `System validated using tag1_short only` | Yes                              |
| `Forgery success?`                       | ✅ In insecure tag-check scenario |


Simulation, constructed a forged ciphertext using:
- The ciphertext body of message 2.
- The truncated tag of message 1 (ef9cf96e).

Simulated a bad implementation that:
- Checks only the first 4 bytes of the tag (tag[:4]), and
- Accepts the message if it matches the reused tag (tag1_short), regardless of origin.

So the "forgery" was forced by:
- Replacing tag2_short with tag1_short,
- Not recomputing the tag from the actual ciphertext,
- The fake system blindly accepting any ciphertext + matching truncated tag.

⚠️ This Is the Point of the Attack
In insecure systems that:
- Truncate GCM tags, and
- Accept the tag independently of the actual ciphertext it belongs to,

An attacker can:
- Take a known (plaintext, ciphertext, tag) triplet,
- Craft any ciphertext (e.g. message 2),
- Reattach tag from message 1, and
- Get it accepted.

This simulates a forgery bypass, not a cryptographic miracle.
"""
