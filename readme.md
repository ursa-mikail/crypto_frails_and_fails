# 💣 Weakening On Crypto Frails and Fails 
🔐 Cryptographic Attack Demos & Vulnerability Simulations

This repository is a curated collection of Python-based demonstrations simulating vulnerabilities and attacks across different cryptographic primitives, modes, and implementation scenarios.

Each folder includes scripts and visualizations to help you understand where and how cryptographic schemes can fail—when used incorrectly, implemented poorly, or under specific threat models.

Each of these showcases a “don’t do this in production” anti-pattern:

| Folder                  | Description                                                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **CBC/**                | Attacks exploiting the malleability of Cipher Block Chaining (CBC) mode (e.g., POODLE, tampering without integrity). |
| **ECB/**                | Visualization and demonstration of Electronic Codebook (ECB) mode weaknesses—especially pattern leakage.             |
| **GCM/**                | Simulated attacks on AES-GCM, including tag forgery through collisions and weakened tags.                            |
| **GCM\_CTR/**           | Dangers of nonce reuse in GCM and CTR, showing how it leads to 2-time pad vulnerabilities.                           |
| **RNG/**                | Attacks on random number generators, showing how poor RNGs lead to key recovery and predictability.                  |
| **RSA/**                | Cryptanalytic attacks on RSA, including Hastad’s broadcast attack.                                                   |
| **broken\_RNG/**        | Bruteforce examples targeting weak or linear PRNGs.                                                                  |
| **cache\_and\_timing/** | Cache-based and timing attacks visualized and explained, showcasing side-channel vulnerabilities.                    |

<hr>

## 📚 Recommended Use

📖 Learn: Understand how classical and modern crypto can fail.
🧪 Experiment: Tweak code and run your own variations.
🛡 Defend: Study these to avoid implementing insecure crypto in your own systems.

## ⚠️ Disclaimer
This repository is for educational and ethical use only. The goal is to foster understanding of cryptographic design, not to aid malicious activity.

## 🧠 Credits
Built by practitioners interested in strengthening system security through transparency, experimentation, and shared knowledge.

<hr>

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

![RNG](RNG)

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

![CBC](CBC)

## 🔄 10. Rolling Your Own Crypto

Show a "custom encryption" function.
Break it using statistical analysis.

## 🔄 11. Cache And Timing

Leaky processes. 

Timing attacks: ![cache_and_timing](cache_and_timing)
