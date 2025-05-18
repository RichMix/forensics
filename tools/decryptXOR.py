# Credit to https://medium.com/@seedr1024 page for where I found the script, tested it and confirmed it's success

def find_xor_key_and_decode(encoded_text, known_start, known_end, key_length=5):
    # Convert the encoded text to a list of bytes
    encoded_bytes = bytes.fromhex(encoded_text)
    
    # Convert known letters to their byte representation
    known_start_bytes = known_start.encode()
    known_end_byte = known_end.encode()
    
    # Find the first part of the key by XORing known start bytes with the corresponding encoded bytes
    key_start = bytes([encoded_bytes[i] ^ known_start_bytes[i] for i in range(len(known_start_bytes))])
    
    # Find the last part of the key by XORing the known end byte with the last byte of the encoded text
    key_end = encoded_bytes[-1] ^ known_end_byte[0]
    
    # Assuming the key is repeating and its length is key_length
    key = key_start + bytes([key_end])
    
    # Ensure the key length is exactly key_length
    key = key[:key_length]
    
    # Decode the entire message using the key
    decoded_message = bytes([encoded_bytes[i] ^ key[i % key_length] for i in range(len(encoded_bytes))]).decode('latin1')
    
    return key, decoded_message

# Example usage
encoded_text = input("Enter the encoded text in hexadecimal: ")
known_start = input("Enter the first 4 known letters: ")
known_end = input("Enter the last known letter: ")

key, decoded_message = find_xor_key_and_decode(encoded_text, known_start, known_end)
print("The XOR key is:", key.decode('latin1'))  # Use 'latin1' to safely decode bytes to string
print("The decoded message is:", decoded_message)
