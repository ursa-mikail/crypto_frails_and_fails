from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from collections import defaultdict

# Setup: AES-GCM with 32-bit tags (for collision simulation)
KEY = AESGCM.generate_key(bit_length=128)
aesgcm = AESGCM(KEY)

TAG_BITS = 32  # Truncate 128-bit tag to 32 bits for birthday effect
TAG_BYTES = TAG_BITS // 8
NUM_MESSAGES = 2**20
# Fixed nonce (to simulate misuse) – realistic tag collision only under same nonce
NONCE = os.urandom(12)

seen_tags = dict()

def hex_diff(a: bytes, b: bytes) -> str:
    """Return visual diff of hex bytes"""
    return ''.join(f'^{b1:02x}' if b1 != b2 else f'  ' for b1, b2 in zip(a, b))

print(f"🔐 AES-GCM tag collision simulation with {TAG_BITS}-bit truncated tags")

for i in range(NUM_MESSAGES):
    msg = os.urandom(32)
    aad = b"auth"
    ciphertext = aesgcm.encrypt(NONCE, msg, aad)
    
    full_tag = ciphertext[-16:]  # last 16 bytes is tag
    short_tag = full_tag[:TAG_BYTES]
    tag_hex = short_tag.hex()

    if tag_hex in seen_tags:
        # Collision found!
        prev = seen_tags[tag_hex]
        prev_msg = prev["msg"]
        prev_ct = prev["ct"]

        print(f"\n⚠️ COLLISION FOUND at #{i + 1}")
        print(f"🔑 Truncated Tag: {tag_hex}")
        print(f"📝 Message A:     {prev_msg.hex()}")
        print(f"📝 Message B:     {msg.hex()}")
        print(f"📍 Hex Diff:      {hex_diff(prev_msg, msg)}") # diff showing how they differ (bit/hex diff).
        print(f"📦 Ciphertext A:  {prev_ct.hex()}")
        print(f"📦 Ciphertext B:  {ciphertext.hex()}")
        break

    seen_tags[tag_hex] = {"msg": msg, "ct": ciphertext}
else:
    print("\n✅ No collisions found (try more messages or smaller tag size)")

"""
With a 32-bit tag, the birthday bound hits around 2**16 messages.
With 128-bit tags (real GCM), the bound is ∼2**64 — far too large to simulate without a supercomputer.

1. The tag is what collides (used to authenticate the ciphertext).
2. The messages are different (even slightly), yet their tags match after truncation.
3. In real AES-GCM with 128-bit tags, this happens only after ≈2⁶⁴ encryptions per nonce.
4. We simulate this faster by truncating the tag to 32 bits.

🔐 AES-GCM tag collision simulation with 32-bit truncated tags

⚠️ COLLISION FOUND at #66822
🔑 Truncated Tag: a870fbe0
📝 Message A:     93693c7407a825b39b6c5c36e41c4890525bbc2b4f05e661dd88d58f6b575501
📝 Message B:     00e0cb44bdbd9c3e8c6530ff383c17f668404ece5d4e9f47aa33ae6ff8a62318
📍 Hex Diff:      ^93^69^3c^74^07^a8^25^b3^9b^6c^5c^36^e4^1c^48^90^52^5b^bc^2b^4f^05^e6^61^dd^88^d5^8f^6b^57^55^01
📦 Ciphertext A:  e758565b13989cc72d9ea773d4af426a639acab8994cc202dd2429a09de02328a870fbe0fe41677165d005769974cc8e
📦 Ciphertext B:  74d1a16ba98d254a3a97cbba088f1d0c5981385d8b07bb24aa9f52400e115531a870fbe0a20d6f5efae3ef597a6a5427

"""

collisions = defaultdict(list)

print(f"Simulating tag collisions with {TAG_BITS}-bit tags and fixed nonce...")

for i in range(NUM_MESSAGES):
    msg = os.urandom(32)
    aad = b"auth"

    # Encrypt and truncate the tag
    ciphertext = aesgcm.encrypt(NONCE, msg, aad)
    tag = ciphertext[-16:]  # AES-GCM default tag is 16 bytes
    truncated_tag = tag[:TAG_BYTES]

    # Check for collision
    tag_hex = truncated_tag.hex()
    if tag_hex in collisions:
        print(f"\n⚠️ Collision found after {i+1} messages!")
        print(f"Previous message: {collisions[tag_hex]}")
        print(f"New message: {msg.hex()}")
        break

    collisions[tag_hex].append(msg)

else:
    print("\n✅ No collisions found (yet). Try increasing NUM_MESSAGES or lowering TAG_BITS.")

"""
Simulating tag collisions with 32-bit tags and fixed nonce...

⚠️ Collision found after 75179 messages!
Previous message: [b'f\xb1\xec\x9b\xb5\xcca7J\x8b\xc6\x9f\x91\x13<8\x1f\x8e\x1c\xe4ZHhC\xdc\x8e3\xebg\x94\x84K']
New message: b03a3b6cf867e7e94c281d4237413f90bc99b51ac49ecdd2a4a8aa3a0d176751
"""

# Fixed nonce (to simulate misuse scenario)
NONCE = os.urandom(12)
collisions = dict()

print(f"Running AES-GCM tag collision demo with {TAG_BITS}-bit tags and fixed nonce...")

for i in range(NUM_MESSAGES):
    msg = os.urandom(32)  # Random 32-byte message
    aad = b"auth"

    ciphertext = aesgcm.encrypt(NONCE, msg, aad)
    tag_full = ciphertext[-16:]
    truncated_tag = tag_full[:TAG_BYTES]
    tag_hex = truncated_tag.hex()

    if tag_hex in collisions:
        prev_msg = collisions[tag_hex]['msg']
        prev_ct = collisions[tag_hex]['ciphertext']

        print(f"\n⚠️  Tag collision found after {i + 1} messages!")
        print(f"🔐 Truncated tag: {tag_hex}")
        print(f"📝 Message 1: {prev_msg.hex()}")
        print(f"📦 Ciphertext 1: {prev_ct.hex()}")
        print(f"📝 Message 2: {msg.hex()}")
        print(f"📦 Ciphertext 2: {ciphertext.hex()}")
        break
    else:
        collisions[tag_hex] = {'msg': msg, 'ciphertext': ciphertext}

else:
    print("\n✅ No tag collisions found after full run. Try more messages or a smaller tag size.")

"""
🔍 
- The truncated authentication tag is the same, even though the messages and ciphertexts differ.
- In real-world AES-GCM, tag is 128-bit — you’d need ∼2**64  encryptions before seeing this naturally.
- Shows why integrity guarantee weakens after you push past birthday bounds, especially under nonce reuse.

Running AES-GCM tag collision demo with 32-bit tags and fixed nonce...

⚠️  Tag collision found after 49643 messages!
🔐 Truncated tag: 662ac295
📝 Message 1: ac9d5af9a7716a4be7c553034e29c318ebb78381fb57801f9840b482b8a45985
📦 Ciphertext 1: 7d9319ccbc5a6ae4509490b730c77a98299e02e58322241b66b40dcaa0aeec0e662ac295225ec0886f8cb770905caafa
📝 Message 2: 6c6bbe1fd9046358d7a3d91b0e48fe6d4bf662444ca332095fe5c6691c21a84f
📦 Ciphertext 2: bd65fd2ac22f63f760f21aaf70a647ed89dfe32034d6960da1117f21042b1dc4662ac295e974bc71d2f07e2a9be236d6
"""