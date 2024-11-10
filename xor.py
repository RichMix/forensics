# xor.py

import binascii

# Encrypted data in hexadecimal format 
encrypted_data_hex = "cfac ef32 574f 205e e1fa bb74 0931 533f fe98".replace(" ", "")
encrypted_data = bytes.fromhex(encrypted_data_hex)

# Step 1: Extract Version and Flag Length
version_number = encrypted_data[0]  # First byte
flag_length_bytes = encrypted_data[1:5]  # Next four bytes (big-endian)
flag_length = int.from_bytes(flag_length_bytes, byteorder='big')

# Step 2: Extract Encrypted Flag Data
encrypted_flag_data = encrypted_data[5:5 + flag_length]

# Step 3: XOR Key Deduction (Assume "FLAG{" prefix)
known_prefix = b"FLAG{"
xor_key = bytes([encrypted_flag_data[i] ^ known_prefix[i] for i in range(len(known_prefix))])

# Step 4: Expand XOR Key
full_xor_key = (xor_key * (len(encrypted_flag_data) // len(xor_key))) + xor_key[:len(encrypted_flag_data) % len(xor_key)]

# Step 5: Decrypt Flag
decrypted_flag = bytes([encrypted_flag_data[i] ^ full_xor_key[i] for i in range(len(encrypted_flag_data))])

# Results
first_byte_of_xor_key = hex(xor_key[0])  # Q1: First byte of XOR key
full_xor_key_hex = binascii.hexlify(xor_key).decode()  # Q2: Full XOR key in hex
plaintext_flag = decrypted_flag.decode()  # Q3: Plaintext flag

print("Q1 - First byte of XOR key:", first_byte_of_xor_key)
print("Q2 - Full XOR key (hex):", full_xor_key_hex)
print("Q3 - Plaintext Flag:", plaintext_flag)
