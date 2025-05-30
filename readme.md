# 💣 Weakening On Crypto Frails and Fails 

Each of these showcases a “don’t do this in production” anti-pattern:

## 🔐 1. Truncated GCM Tag Demo

Show AES-GCM with 32/64-bit auth tags instead of 128-bit.

Attack simulation: brute-force tag recovery on small plaintexts.
![GCM](GCM)

## 📦 2. Reused Nonce (IV) in AES-GCM or AES-CTR

Encrypt 2 messages with the same IV.
Show how XORing ciphertexts leaks plaintext info.
![GCM_CTR](GCM_CTR)

## 🔁 3. ECB Mode

Encrypt an image (e.g., Tux or Mona Lisa) with AES-ECB.
Reveal repeating patterns that leak structure.
![ECB](ECB)

## 📉 4. Hardcoded Keys

Show code with hardcoded symmetric keys or RSA private keys.
Demonstrate recovery of plaintext or impersonation.

## 📅 5. Predictable RNG

Use rand() or other weak PRNGs to generate keys/IVs.
Show brute-force recovery of keys from low entropy.

## 🧱 6. RSA with Small Exponent (e = 3)

Encrypt the same plaintext across 3 public keys (Håstad’s Broadcast Attack).

Recover plaintext without private keys.
![RSA](RSA)

## 🧮 7. Padding Oracle Attack Demo

Use AES-CBC with PKCS#7 padding.
Simulate a padding oracle and show plaintext recovery.
![CBC](CBC)

## 💬 8. Insecure Hashes

Use MD5/SHA1 for signing or file integrity.
Demonstrate hash collision with chosen inputs.

## 🛑 9. Lack of Authenticated Encryption

Use AES-CBC without HMAC.
Tamper with ciphertext and show no detection.

## 🔄 10. Rolling Your Own Crypto

Show a "custom encryption" function.
Break it using statistical analysis.

