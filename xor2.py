import binascii

# Encrypted data in hexadecimal format (already provided in the structure)
encrypted_data_hex = "cfac ef32 574f 205e e1fa bb74 0931 533f fe98".replace(" ", "")
encrypted_data = bytes.fromhex(encrypted_data_hex)

try:
    # Step 1: Extract Version and Flag Length
    version_number = encrypted_data[0]  # First byte
    flag_length_bytes = encrypted_data[1:5]  # Next four bytes (big-endian)
    flag_length = int.from_bytes(flag_length_bytes, byteorder='big')

    # Step 2: Extract Encrypted Flag Data
    encrypted_flag_data = encrypted_data[5:5 + flag_length]

    # Step 3: Define the Known XOR Key Length
    xor_key_length = 8  # As specified by the documentation

    # Step 4: Deduce the XOR Key
    # We'll assume the key length is 8 bytes and reuse it as needed
    xor_key = encrypted_data[:xor_key_length]  # Extract first 8 bytes for the XOR key

    # Step 5: Expand XOR Key
    full_xor_key = (xor_key * (len(encrypted_flag_data) // xor_key_length)) + xor_key[:len(encrypted_flag_data) % xor_key_length]

    # Step 6: Decrypt Flag
    decrypted_flag = bytes([encrypted_flag_data[i] ^ full_xor_key[i] for i in range(len(encrypted_flag_data))])

    # Results
    first_byte_of_xor_key = hex(xor_key[0])  # Q1: First byte of XOR key
    full_xor_key_hex = binascii.hexlify(xor_key).decode()  # Q2: Full XOR key in hex

    # Attempt to decode the decrypted flag with error handling
    try:
        plaintext_flag = decrypted_flag.decode('utf-8')  # Primary attempt with utf-8
    except UnicodeDecodeError:
        plaintext_flag = decrypted_flag.decode('latin-1')  # Fallback to latin-1 if utf-8 fails

    print("Q1 - First byte of XOR key:", first_byte_of_xor_key)
    print("Q2 - Full XOR key (hex):", full_xor_key_hex)
    print("Q3 - Plaintext Flag:", plaintext_flag)

except IndexError:
    print("Error: Encrypted data is too short or flag length exceeds available data.")
except UnicodeDecodeError:
    print("Error: Unable to decode the decrypted flag, even with fallback encoding.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
