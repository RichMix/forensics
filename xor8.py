import binascii

# Encrypted data in hexadecimal format
encrypted_data_hex = "cfac ef32 574f 205e e1fa bb74 0931 533f fe98".replace(" ", "")
encrypted_data = bytes.fromhex(encrypted_data_hex)

try:
    # Step 1: Extract version number
    version_number = encrypted_data[0]
    print("Version Number:", version_number)

    # Step 2: Extract flag length (next 4 bytes)
    flag_length_bytes = encrypted_data[1:5]
    flag_length = int.from_bytes(flag_length_bytes, byteorder='big')
    print("Flag Length:", flag_length, "bytes")

    # Step 3: Verify the flag length against remaining data
    if len(encrypted_data) < 5 + flag_length:
        raise ValueError(f"Error: Flag length ({flag_length} bytes) exceeds available encrypted data ({len(encrypted_data) - 5} bytes).")

    # Step 4: Extract encrypted flag data
    encrypted_flag_data = encrypted_data[5:5 + flag_length]
    print("Encrypted Flag Data (hex):", binascii.hexlify(encrypted_flag_data).decode())

    # Known Prefix "SKY-" for deriving the XOR key
    known_prefix = b"SKY-"
    
    # Step 5: Derive XOR Key
    xor_key_start = [0xcc]
    xor_key_rest = [encrypted_flag_data[i] ^ known_prefix[i] for i in range(len(known_prefix))]
    xor_key = bytes(xor_key_start + xor_key_rest)
    print("Initial XOR Key (hex):", binascii.hexlify(xor_key).decode())
    
    # Expand XOR Key to match the flag length
    full_xor_key = (xor_key * (len(encrypted_flag_data) // len(xor_key))) + xor_key[:len(encrypted_flag_data) % len(xor_key)]
    print("Full XOR Key (hex):", binascii.hexlify(full_xor_key).decode())
    
    # Step 6: Decrypt the flag
    decrypted_flag = bytes([encrypted_flag_data[i] ^ full_xor_key[i] for i in range(len(encrypted_flag_data))])
    plaintext_flag = decrypted_flag.decode(errors='replace')  # Decode to text, replacing undecodable characters

    # Results
    print("Q1 - First byte of XOR key:", hex(xor_key[0]))
    print("Q2 - Full XOR key (hex):", binascii.hexlify(full_xor_key).decode())
    print("Q3 - Plaintext Flag:", plaintext_flag)

except Exception as e:
    print("Error:", e)
