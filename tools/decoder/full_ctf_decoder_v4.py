# full_ctf_decoder_v4.py
import base64, re, string, argparse
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

def rot5(text: str) -> str:
    return ''.join(chr((ord(c)-48+5)%10+48) if c.isdigit() else c for c in text)

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

def post_morse_rot(text: str, shift: int) -> str:
    decoded = decode_morse(text)
    return rot(decoded, shift)

def rail_fence_decrypt(cipher: str, num_rails: int) -> str:
    fence = [['' for _ in range(len(cipher))] for _ in range(num_rails)]
    rail, var = 0, 1
    for i in range(len(cipher)):
        fence[rail][i] = '*'
        rail += var
        if rail == 0 or rail == num_rails-1:
            var = -var
    index = 0
    for r in range(num_rails):
        for c in range(len(cipher)):
            if fence[r][c] == '*' and index < len(cipher):
                fence[r][c] = cipher[index]
                index += 1
    result = []
    rail, var = 0, 1
    for i in range(len(cipher)):
        result.append(fence[rail][i])
        rail += var
        if rail == 0 or rail == num_rails-1:
            var = -var
    return ''.join(result)

def brute_force_rail_fence(cipher: str, max_rails=10) -> List[str]:
    results = []
    for rails in range(2, max_rails + 1):
        results.append(f"Rails {rails:02}: {rail_fence_decrypt(cipher, rails)}")
    return results

def run_all_decoders(text: str) -> List[str]:
    outputs = []
    outputs.append("================ ROT Shifts ===============")
    for i in range(1, 26):
        outputs.append(f"ROT{i:02}: {rot(text, i)}")
    outputs.append("\n================ ROT5 =====================")
    outputs.append(rot5(text))
    outputs.append("\n================ Atbash ===================")
    outputs.append(atbash(text))
    outputs.append("\n================ Morse =====================")
    morse = decode_morse(text)
    outputs.append(morse)
    outputs.append("\n========= Morse then ROT9 =================")
    outputs.append(post_morse_rot(text, 9))
    outputs.append("\n================ Binary ====================")
    outputs.append(decode_binary(text))
    outputs.append("\n================ Hex =======================")
    outputs.append(decode_hex(text))
    outputs.append("\n================ Base64 ====================")
    outputs.append(decode_base64(text))
    outputs.append("\n================ ASCII =====================")
    outputs.append(decode_ascii(text))
    outputs.append("\n=========== Rail Fence (2–10 rails) =========")
    outputs.extend(brute_force_rail_fence(text))
    return outputs

def main():
    parser = argparse.ArgumentParser(description="CTF Auto Decoder v4")
    parser.add_argument('--input', nargs='+', help='Text to decode')
    args = parser.parse_args()

    if not args.input:
        print("Usage: python3 full_ctf_decoder_v4.py --input <string>")
        return

    text = ' '.join(args.input)
    results = run_all_decoders(text)
    for result in results:
        print(result)

if __name__ == '__main__':
    main()
