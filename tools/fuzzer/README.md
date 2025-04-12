
# 🛡️ LFI Fuzzer Tool

This Python script is a reusable tool for detecting Local File Inclusion (LFI) vulnerabilities in web applications via URL query parameters (e.g., `filename=...`).

## 🔧 How to Use

1. **Edit the script:**
   - Set the `TARGET_URL` variable to your target endpoint.
   - Example: `"https://target.site/dog?filename="`

2. **Run the script:**
```bash
python3 lfi_fuzzer.py
```

3. **Output:**
   - It will print out potential flag contents, secrets, or keys found through traversal.

## ⚙️ Features

- Automatic traversal up to 6 directory levels (`../`)
- Scans for common sensitive files (`flag.txt`, `.env`, `config.php`, etc.)
- Highlights matches with keywords like `flag`, `key`, `Liber8`, and `{`
- Clean and readable terminal output
- URL-encodes inputs for safe request formatting

---

## 🧠 Use Case: CTF Write-up (Liber8Dogs - 100 pts)

**Challenge:**  
> "Liber8tion posted dog photos via `/dog?filename=...`. Find the flag."

**Exploit Path:**
1. Identified vulnerable endpoint: `/dog`
2. Discovered the app resolves files relative to `/app/static/dogs/`
3. Used `../../../flag.txt` to successfully access `/flag.txt` from root
4. Retrieved the flag: `SKY-BUPE-2348`

**Payload:**
```bash
curl "https://site/dog?filename=../../../flag.txt"
```

**Root Cause:**
> The application trusted user-supplied file paths, using them directly in file access without sanitization.

---

## 📁 Files Included

- `lfi_fuzzer.py` – Python script to automate the fuzzing
- `README.md` – This file
- `writeup.txt` – CTF write-up example based on Liber8Dogs challenge

