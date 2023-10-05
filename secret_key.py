from cryptography.fernet import Fernet

# Generate a key and save it securely.
key = Fernet.generate_key()
with open("secret.key", "wb") as key_file:
    key_file.write(key)

# Encrypt the API secret key
cipher_suite = Fernet(key)
ciphered_text = cipher_suite.encrypt(b"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")
with open("encrypted_api_key.txt", "wb") as encrypted_file:
    encrypted_file.write(ciphered_text)