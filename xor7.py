import binascii

# Encrypted data in hexadecimal format
encrypted_data_hex = "cfac ef32 574f 205e e1fa bb74 0931 533f fe98".replace(" ", "")
encrypted_data = bytes.fromhex(encrypted_data_hex)

try:
    # Step 1: Extract version number and flag length
    version_number = encrypted_data[0]
    flag_length_bytes = encrypted_data[1:5]
    flag_length = int.from_bytes(flag_length_bytes, byteorder='big')

    # Step 2: Verify the flag length against remaining data
    if len(encrypted_data) < 5 + flag_length:
        raise ValueError("Error: Flag length exceeds available encrypted data.")

    # Step 3: Extract encrypted flag data
    encrypted_flag_data = encrypted_data[5:5 + flag_length]

    # Known Prefix "SKY-" for deriving the XOR key
    known_prefix = b"SKY-"
    
    # Step 4: Derive XOR Key
    xor_key_start = [0xcc]
    xor_key_rest = [encrypted_flag_data[i] ^ known_prefix[i] for i in range(len(known_prefix))]
    xor_key = bytes(xor_key_start + xor_key_rest)
    
    # Expand XOR Key to the full 8 bytes (assumed repetitive pattern)
    full_xor_key = (xor_key * (len(encrypted_flag_data) // len(xor_key))) + xor_key[:len(encrypted_flag_data) % len(xor_key)]
    
    # Step 5: Decrypt the flag
    decrypted_flag = bytes([encrypted_flag_data[i] ^ full_xor_key[i] for i in range(len(encrypted_flag_data))])

    # Display results
    first_byte_of_xor_key = hex(xor_key[0])  # Q1: First byte of XOR key
    full_xor_key_hex = binascii.hexlify(xor_key).decode()  # Q2: Full XOR key in hex
    plaintext_flag = decrypted_flag.decode(errors='replace')  # Q3: Plaintext flag, replace undecodable bytes

    print("Q1 - First byte of XOR key:", first_byte_of_xor_key)
    print("Q2 - Full XOR key (hex):", full_xor_key_hex)
    print("Q3 - Plaintext Flag:", plaintext_flag)

except Exception as e:
    print("Error:", e)
