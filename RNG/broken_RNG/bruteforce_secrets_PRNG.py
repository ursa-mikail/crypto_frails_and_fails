#!pip install faker
"""
Uses faker to generate the original word and candidate words.
Filters candidates by the starting letter hint.
Hashes each candidate word and compares it to the target hash.
Uses tqdm to show progress (install with pip install tqdm if needed).
"""
import hashlib
import faker
import string
from tqdm import tqdm

# Initialize faker
fake = faker.Faker()

# Generate a random word
word = fake.word()
print(f"[+] Generated word: {word}")

hint = word[0]
hashed = hashlib.sha256(word.encode()).hexdigest()

print(f"[+] SHA-256 Hash: {hashed}")
print(f"[+] Hint: Word starts with '{hint}'")

# Brute-force from dictionary of faker words (realistic subset)
print("[*] Starting brute-force search...")
found = False

# Create a list of candidate words that start with the hint
candidate_words = [fake.word() for _ in range(5000)]
candidate_words = list(set(candidate_words))  # Remove duplicates
candidate_words = [w for w in candidate_words if w.startswith(hint)]

for w in tqdm(candidate_words):
    if hashlib.sha256(w.encode()).hexdigest() == hashed:
        print(f"[+] Found! The word is: {w}")
        found = True
        break

if not found:
    print("[-] Word not found in generated candidates.")

"""
[+] Generated word: hospital
[+] SHA-256 Hash: 8afe3c83decffdf6dc48597a3f1a52be7c6e2b97b4bdf3b15e20a87a1f657f01
[+] Hint: Word starts with 'h'
[*] Starting brute-force search...
 84%|████████▍ | 31/37 [00:00<00:00, 63179.51it/s][+] Found! The word is: hospital
""" 