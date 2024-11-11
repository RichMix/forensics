import binascii

# Encrypted data in hexadecimal format
encrypted_data_hex = "cfac ef32 574f 205e e1fa bb74 0931 533f fe98".replace(" ", "")
encrypted_data = bytes.fromhex(encrypted_data_hex)

try:
    # Extract Encrypted Flag Data (skip any length or version handling)
    encrypted_flag_data = encrypted_data[1:]  # Start from the second byte to avoid initial version byte

    # Known Prefix "SKY" (first 3 bytes of the flag)
    known_prefix = b"SKY"

    # Derive XOR Key from Known Prefix
    xor_key = bytes([encrypted_flag_data[i] ^ known_prefix[i] for i in range(len(known_prefix))])

    # Expand XOR Key across the length of the encrypted flag data
    full_xor_key = (xor_key * (len(encrypted_flag_data) // len(xor_key))) + xor_key[:len(encrypted_flag_data) % len(xor_key)]

    # Decrypt Flag
    decrypted_flag = bytes([encrypted_flag_data[i] ^ full_xor_key[i] for i in range(len(encrypted_flag_data))])

    # Display results
    first_byte_of_xor_key = hex(xor_key[0])  # First byte of XOR key
    full_xor_key_hex = binascii.hexlify(full_xor_key).decode()  # Full XOR key in hex
    plaintext_flag = decrypted_flag.decode(errors='replace')  # Decode to text, replacing undecodable characters

    print("Q1 - First byte of XOR key:", first_byte_of_xor_key)
    print("Q2 - Full XOR key (hex):", full_xor_key_hex)
    print("Q3 - Plaintext Flag:", plaintext_flag)

except Exception as e:
    print("Error:", e)
