#  If we can find a natural collision for a hash, such as H(a)=H(b), we can also create a hash for H(a || c) = H(b || c) 
import hashlib

def show_hex_diff(block_a, block_b):
    # Convert each line into raw bytes
    def to_bytes(lines):
        return bytes.fromhex(''.join(lines).replace(' ', ''))

    ba = to_bytes(block_a)
    bb = to_bytes(block_b)

    print("Hex Difference (byte-by-byte):")
    print("-" * 60)
    for i in range(0, len(ba), 16):
        a_chunk = ba[i:i+16]
        b_chunk = bb[i:i+16]
        if a_chunk != b_chunk:
            a_hex = ' '.join(f'{b:02x}' for b in a_chunk)
            b_hex = ' '.join(f'{b:02x}' for b in b_chunk)
            print(f'Offset {i:04x}:')
            print(f'  A: {a_hex}')
            print(f'  B: {b_hex}')
            print()

def ansi_colored_hex_diff(block_a, block_b):
    def to_bytes(lines):
        return bytes.fromhex(''.join(lines).replace(' ', ''))

    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

    ba = to_bytes(block_a)
    bb = to_bytes(block_b)

    print("Hex Difference with Raw ANSI Colors:")
    print("-" * 80)
    for i in range(0, len(ba), 16):
        a_chunk = ba[i:i+16]
        b_chunk = bb[i:i+16]

        if a_chunk != b_chunk:
            print(f"Offset {i:04x}:")
            a_line = []
            b_line = []
            for j in range(len(a_chunk)):
                byte_a = a_chunk[j]
                byte_b = b_chunk[j]
                if byte_a != byte_b:
                    a_line.append(f'{RED}{byte_a:02x}{RESET}')
                    b_line.append(f'{GREEN}{byte_b:02x}{RESET}')
                else:
                    a_line.append(f'{byte_a:02x}')
                    b_line.append(f'{byte_b:02x}')
            print("  A:", ' '.join(a_line))
            print("  B:", ' '.join(b_line))
            print()

from IPython.display import display, HTML

def html_colored_hex_diff(block_a, block_b):
    def to_bytes(lines):
        return bytes.fromhex(''.join(lines).replace(' ', ''))

    ba = to_bytes(block_a)
    bb = to_bytes(block_b)

    html = "<h3>Hex Difference with Color Highlighting</h3>"
    html += "<style> .diff { font-family: monospace; white-space: pre; } .red {color:red;} .green {color:green;} </style><div class='diff'>"

    for i in range(0, len(ba), 16):
        a_chunk = ba[i:i+16]
        b_chunk = bb[i:i+16]

        if a_chunk != b_chunk:
            html += f"<b>Offset {i:04x}:</b><br>"
            a_line = []
            b_line = []

            for j in range(len(a_chunk)):
                byte_a = a_chunk[j]
                byte_b = b_chunk[j]
                if byte_a != byte_b:
                    a_line.append(f"<span class='red'>{byte_a:02x}</span>")
                    b_line.append(f"<span class='green'>{byte_b:02x}</span>")
                else:
                    a_line.append(f"{byte_a:02x}")
                    b_line.append(f"{byte_b:02x}")

            html += "A: " + ' '.join(a_line) + "<br>"
            html += "B: " + ' '.join(b_line) + "<br><br>"

    html += "</div>"
    display(HTML(html))


def from_hex_blob(hex_lines):
    # Join all hex strings, remove spaces, convert to bytes
    hex_str = ''.join(hex_lines).replace(' ', '')
    return bytes.fromhex(hex_str)

# First colliding block ("a")
block_a = [
    'd131dd02c5e6eec4693d9a0698aff95c 2fcab58712467eab4004583eb8fb7f89',
    '55ad340609f4b30283e488832571415a 085125e8f7cdc99fd91dbdf280373c5b',
    'd8823e3156348f5bae6dacd436c919c6 dd53e2b487da03fd02396306d248cda0',
    'e99f33420f577ee8ce54b67080a80d1e c69821bcb6a8839396f9652b6ff72a70'
]

# Second colliding block ("b")
block_b = [
    'd131dd02c5e6eec4693d9a0698aff95c 2fcab50712467eab4004583eb8fb7f89',
    '55ad340609f4b30283e4888325f1415a 085125e8f7cdc99fd91dbd7280373c5b',
    'd8823e3156348f5bae6dacd436c919c6 dd53e23487da03fd02396306d248cda0',
    'e99f33420f577ee8ce54b67080280d1e c69821bcb6a8839396f965ab6ff72a70'
]

if block_a != block_b:
    print("Contents of block_a and block_b differ.")
    html_colored_hex_diff(block_a, block_b)

data_a = from_hex_blob(block_a)
data_b = from_hex_blob(block_b)

hash_a = hashlib.md5(data_a).hexdigest()
hash_b = hashlib.md5(data_b).hexdigest()

print("MD5(data_a):", hash_a)
print("MD5(data_b):", hash_b)
print("Collision:", hash_a == hash_b)

# Optional: Test H(a || c) == H(b || c)
suffix = b"hello-world"
combined_a = data_a + suffix
combined_b = data_b + suffix

hash_combined_a = hashlib.md5(combined_a).hexdigest()
hash_combined_b = hashlib.md5(combined_b).hexdigest()

print("\nMD5(data_a || suffix):", hash_combined_a)
print("MD5(data_b || suffix):", hash_combined_b)
print("Extended collision:", hash_combined_a == hash_combined_b)

"""
Contents of block_a and block_b differ.
Hex Difference with Color Highlighting
Offset 0010:
A: 2f ca b5 87 12 46 7e ab 40 04 58 3e b8 fb 7f 89
B: 2f ca b5 07 12 46 7e ab 40 04 58 3e b8 fb 7f 89

Offset 0020:
A: 55 ad 34 06 09 f4 b3 02 83 e4 88 83 25 71 41 5a
B: 55 ad 34 06 09 f4 b3 02 83 e4 88 83 25 f1 41 5a

Offset 0030:
A: 08 51 25 e8 f7 cd c9 9f d9 1d bd f2 80 37 3c 5b
B: 08 51 25 e8 f7 cd c9 9f d9 1d bd 72 80 37 3c 5b

Offset 0050:
A: dd 53 e2 b4 87 da 03 fd 02 39 63 06 d2 48 cd a0
B: dd 53 e2 34 87 da 03 fd 02 39 63 06 d2 48 cd a0

Offset 0060:
A: e9 9f 33 42 0f 57 7e e8 ce 54 b6 70 80 a8 0d 1e
B: e9 9f 33 42 0f 57 7e e8 ce 54 b6 70 80 28 0d 1e

Offset 0070:
A: c6 98 21 bc b6 a8 83 93 96 f9 65 2b 6f f7 2a 70
B: c6 98 21 bc b6 a8 83 93 96 f9 65 ab 6f f7 2a 70

MD5(data_a): 79054025255fb1a26e4bc422aef54eb4
MD5(data_b): 79054025255fb1a26e4bc422aef54eb4
Collision: True

MD5(data_a || suffix): 7ca1171ad9cbf8193227a171a46083f1
MD5(data_b || suffix): 7ca1171ad9cbf8193227a171a46083f1
Extended collision: True
"""