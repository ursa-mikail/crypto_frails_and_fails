from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
import numpy as np
import requests
import io
import matplotlib.pyplot as plt

def encrypt_image_ecb(input_image, key):
    img = input_image.convert('RGB')
    data = np.array(img)
    raw_bytes = data.tobytes()
    padded_bytes = pad(raw_bytes, AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded_bytes)
    encrypted = encrypted[:len(raw_bytes)]
    enc_array = np.frombuffer(encrypted, dtype=np.uint8)
    enc_array = enc_array.reshape(data.shape)
    return Image.fromarray(enc_array, 'RGB')

def encrypt_image_cbc(input_image, key, iv):
    img = input_image.convert('RGB')
    data = np.array(img)
    raw_bytes = data.tobytes()
    padded_bytes = pad(raw_bytes, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded_bytes)
    encrypted = encrypted[:len(raw_bytes)]
    enc_array = np.frombuffer(encrypted, dtype=np.uint8)
    enc_array = enc_array.reshape(data.shape)
    return Image.fromarray(enc_array, 'RGB')

if __name__ == "__main__":
    key = b'ThisIsA16ByteKey'
    iv = b'InitializationVe'  # 16 bytes IV for CBC mode

    url = 'https://upload.wikimedia.org/wikipedia/commons/a/af/Tux.png'
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))

    encrypted_ecb = encrypt_image_ecb(image, key)
    encrypted_cbc = encrypt_image_cbc(image, key, iv)

    # Plot original, ECB, and CBC images side by side
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].imshow(image)
    axs[0].set_title('Original Image')
    axs[0].axis('off')

    axs[1].imshow(encrypted_ecb)
    axs[1].set_title('Encrypted Image (AES-ECB)')
    axs[1].axis('off')

    axs[2].imshow(encrypted_cbc)
    axs[2].set_title('Encrypted Image (AES-CBC)')
    axs[2].axis('off')

    plt.show()

