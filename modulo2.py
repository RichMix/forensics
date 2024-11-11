# Given encrypted message as a list of numbers
encrypted_message = [
    630, 471, 514, 336, 688, 758, 957, 619, 165, 750, 228, 614, 141, 546, 
    552, 671, 440, 393, 590, 171, 863, 643, 136, 113, 721, 495, 307, 397
    # Add remaining numbers from the original encrypted message
]

# Function to decrypt using modulo 26
def decrypt_with_mod26(encrypted_message):
    return ''.join(chr((num % 26) + ord('A')) for num in encrypted_message)

# Function to decrypt using modulo 10
def decrypt_with_mod10(encrypted_message):
    return ''.join(str(num % 10) for num in encrypted_message)

# Apply both decryption methods
decrypted_letters = decrypt_with_mod26(encrypted_message)
decrypted_numbers = decrypt_with_mod10(encrypted_message)

# Display results
print("Decrypted using mod 26:", decrypted_letters)
print("Decrypted using mod 10:", decrypted_numbers)
