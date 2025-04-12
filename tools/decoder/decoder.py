# full_ctf_decoder.py
# Version 0.2

import base64, binascii, string, codecs, re, sys
from typing import List

MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9'
}

def rot(text: str, shift: int) -> str:
    """
    Applies a Caesar cipher (ROT-n) shift to the input text.
    Shifts each alphabetic character forward by the specified number of positions.
    Non-alphabetic characters are left unchanged.

    Args:
        text (str): The input text to shift.
        shift (int): The number of positions to shift each letter.

    Returns:
        str: The shifted result.
    """
    def shift_char(c):
        if c.islower(): return chr((ord(c) - 97 + shift) % 26 + 97)
        if c.isupper(): return chr((ord(c) - 65 + shift) % 26 + 65)
        return c
    return ''.join(shift_char(c) for c in text)

def atbash(text: str) -> str:
    def sub(c):
        if c.islower(): return chr(219 - ord(c))
        if c.isupper(): return chr(155 - ord(c))
        return c
    return ''.join(sub(c) for c in text)

def decode_morse(morse: str) -> str:
    output = []
    unknowns = []
    for code in morse.strip().split():
        if code in MORSE_CODE_DICT:
            output.append(MORSE_CODE_DICT[code])
        else:
            output.append('?')
            unknowns.append(code)
    result = ''.join(output)
    if unknowns:
        result += f"\n[!] Warning: Unrecognized morse codes: {', '.join(unknowns)}"
    return result

def decode_binary(text: str) -> str:
    try:
        text = re.sub(r'[^01\s]', '', text)
        binaries = text.split()
        return ''.join(chr(int(b, 2)) for b in binaries)
    except Exception as e:
        return f'[!] Binary decode failed: {e}'

def decode_hex(text: str) -> str:
    try:
        cleaned = re.sub(r'[^0-9a-fA-F]', '', text)
        return bytes.fromhex(cleaned).decode()
    except Exception as e:
        return f'[!] Hex decode failed: {e}'

def decode_base64(text: str) -> str:
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception as e:
        return f'[!] Base64 decode failed: {e}'

def decode_ascii(text: str) -> str:
    try:
        return ''.join(chr(int(num)) for num in text.strip().split())
    except Exception as e:
        return f'[!] ASCII decode failed: {e}'

def run_all_decoders(text: str) -> List[str]:
    outputs = []
    outputs.append("================ ROT Shifts ===============")
    for i in range(1, 26):
        outputs.append(f"ROT{i:02}: {rot(text, i)}")
    outputs.append("\n================ Atbash ===================")
    outputs.append(atbash(text))
    outputs.append("\n================ Morse =====================")
    outputs.append(decode_morse(text))
    outputs.append("\n================ Binary ====================")
    outputs.append(decode_binary(text))
    outputs.append("\n================ Hex =======================")
    outputs.append(decode_hex(text))
    outputs.append("\n================ Base64 ====================")
    outputs.append(decode_base64(text))
    outputs.append("\n================ ASCII =====================")
    outputs.append(decode_ascii(text))
    return outputs

def main():
    """
    Main function for the CTF Auto Decoder script.
    Parses command-line arguments and runs the input through all decoders.
    Usage example:
        python3 full_ctf_decoder.py --input "encrypted_string"
    """
    import argparse
    parser = argparse.ArgumentParser(description="CTF Auto Decoder")
    parser.add_argument('--input', nargs='+', help='Text to decode')
    args = parser.parse_args()

    if not args.input:
        print("Usage: python3 full_ctf_decoder.py --input <string>")
        return

    text = ' '.join(args.input)
    results = run_all_decoders(text)
    for result in results:
        print(result)

if __name__ == '__main__':
    main()