
# full_ctf_decoder.py
import base64, binascii, string, codecs, re
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
    return ''.join(MORSE_CODE_DICT.get(code, '?') for code in morse.strip().split())

def decode_binary(text: str) -> str:
    try:
        text = re.sub(r'[^01]', '', text)
        return ''.join(chr(int(text[i:i+8], 2)) for i in range(0, len(text), 8))
    except: return '[!] Binary decode failed'

def decode_hex(text: str) -> str:
    try: return bytes.fromhex(text.strip()).decode()
    except: return '[!] Hex decode failed'

def decode_base64(text: str) -> str:
    try: return base64.b64decode(text.encode()).decode()
    except: return '[!] Base64 decode failed'

def decode_ascii(text: str) -> str:
    try: return ''.join(chr(int(num)) for num in text.split())
    except: return '[!] ASCII decode failed'

def run_all_decoders(text: str) -> List[str]:
    outputs = []
    outputs.append(f"[ROT Shifts]:")
    for i in range(1, 26): outputs.append(f"ROT{i:02}: {rot(text, i)}")
    outputs.append(f"\n[Atbash]: {atbash(text)}")
    outputs.append(f"\n[Morse]: {decode_morse(text)}")
    outputs.append(f"\n[Binary]: {decode_binary(text)}")
    outputs.append(f"\n[Hex]: {decode_hex(text)}")
    outputs.append(f"\n[Base64]: {decode_base64(text)}")
    outputs.append(f"\n[ASCII]: {decode_ascii(text)}")
    return outputs

def main():
    import argparse
    parser = argparse.ArgumentParser(description="CTF Auto Decoder")
    parser.add_argument('--input', help='Text to decode')
    args = parser.parse_args()
    if not args.input:
        print("Usage: python3 full_ctf_decoder.py --input <string>")
        return
    results = run_all_decoders(args.input)
    for result in results:
        print(result)

if __name__ == '__main__':
    main()
