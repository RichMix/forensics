# CTF Hash Cracker v2 🔐

A cross-platform, Python-based hash cracking utility that supports MD5, SHA1, and SHA256 hashes using Rockyou and SecLists wordlists.

## Features

- Auto-detects hash types
- Supports one or multiple hashes from file
- Accepts a single wordlist or a directory of `.txt` wordlists
- Outputs cracked hashes to `cracked_results.txt`
- Uses `tqdm` for a clean progress bar

## Requirements

- Python 3.x
- tqdm

Install with:

```bash
pip install tqdm
```

## Usage

Run with:

```bash
python3 ctf_hash_cracker_v2.py
```

You will be prompted to input:

- One or more hashes (or a path to a file containing hashes)
- A path to a wordlist (e.g., `rockyou.txt`) or a directory containing `.txt` files (e.g., `SecLists/Passwords/`)

## Example

```
Enter hash(es): hashes1.txt
Enter wordlist: ./SecLists/Passwords/
```

## Platform Notes

✅ Compatible with:
- Windows 10/11 (via CMD or PowerShell)
- macOS (Terminal)
- Linux (any distro with Python 3)

## Tips

- Make sure `rockyou.txt` is unzipped (`gunzip /usr/share/wordlists/rockyou.txt.gz`)
- Download [SecLists](https://github.com/danielmiessler/SecLists) for a large collection of wordlists

Happy cracking!
