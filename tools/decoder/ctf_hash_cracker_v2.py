import hashlib
import os
import re
from tqdm import tqdm  # pip install tqdm

# Identify the hash type based on length and pattern
def identify_hash(hash_str):
    hash_str = hash_str.strip().lower()
    if re.fullmatch(r'[a-f0-9]{32}', hash_str): return "MD5"
    if re.fullmatch(r'[a-f0-9]{40}', hash_str): return "SHA1"
    if re.fullmatch(r'[a-f0-9]{64}', hash_str): return "SHA256"
    return None

# Compute the hash of the password for the given algorithm
def compute_hash(password, algo):
    password = password.strip().encode()
    if algo == "MD5":
        return hashlib.md5(password).hexdigest()
    elif algo == "SHA1":
        return hashlib.sha1(password).hexdigest()
    elif algo == "SHA256":
        return hashlib.sha256(password).hexdigest()

# Load all .txt wordlists from a given directory recursively
def load_wordlists_from_dir(wordlist_dir):
    wordlist_files = []
    for root, _, files in os.walk(wordlist_dir):
        for file in files:
            if file.endswith(".txt"):
                wordlist_files.append(os.path.join(root, file))
    return wordlist_files

# Attempt to crack hashes using the list of wordlists
def crack_hashes(hash_list, wordlist_files):
    cracked = {}
    for wordlist_path in wordlist_files:
        print(f"\n🔍 Trying: {wordlist_path}")
        try:
            with open(wordlist_path, errors='ignore') as f:
                passwords = [line.strip() for line in f]
            for target_hash in tqdm(hash_list, desc="Progress", unit="hash"):
                if target_hash in cracked:
                    continue
                algo = identify_hash(target_hash)
                if not algo:
                    continue
                for pwd in passwords:
                    if compute_hash(pwd, algo) == target_hash:
                        cracked[target_hash] = pwd
                        print(f"✅ Cracked: {target_hash} → {pwd}")
                        break
        except Exception as e:
            print(f"⚠️ Skipped {wordlist_path}: {e}")
    return cracked

if __name__ == "__main__":
    print("💥 CTF Hash Cracker v2 – Rockyou + SecLists\n")
    hash_input = input("Enter hash(es) separated by commas or a hash file path: ").strip()

    if os.path.exists(hash_input):
        with open(hash_input, "r") as f:
            hash_list = [line.strip() for line in f if line.strip()]
    else:
        hash_list = [h.strip() for h in hash_input.split(",")]

    wordlist_dir = input("Enter wordlist file or directory [default: ./rockyou.txt]: ").strip()
    if not wordlist_dir:
        wordlist_files = ["./rockyou.txt"]
    elif os.path.isdir(wordlist_dir):
        wordlist_files = load_wordlists_from_dir(wordlist_dir)
    else:
        wordlist_files = [wordlist_dir]

    print(f"\n🚀 Starting cracking of {len(hash_list)} hashes using {len(wordlist_files)} wordlist(s)...")
    results = crack_hashes(hash_list, wordlist_files)

    if results:
        with open("cracked_results.txt", "w") as out:
            for h, pwd in results.items():
                out.write(f"{h}:{pwd}\n")
        print("\n✅ Cracked Hashes written to cracked_results.txt")
    else:
        print("❌ No matches found.")
