# POODLE attack
Recovers the entire plaintext, block by block, and asserts that the recovered plaintext matches the original target plaintext.

It loops over all ciphertext blocks, starting from block 1 (the first ciphertext block after IV).
For each block, it performs the padding oracle byte-by-byte attack to recover the plaintext block.
It concatenates all recovered blocks.
It removes padding from the full recovered plaintext.

Finally, asserts the recovered plaintext matches your target_plaintext.
