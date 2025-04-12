# Generated README and CTF write-up along with a commented version of the LFI fuzzer script
readme_content = """
# 🛡️ LFI Fuzzer Tool

This Python script is a reusable tool for detecting Local File Inclusion (LFI) vulnerabilities in web applications via URL query parameters (e.g., `filename=...`).

## 🔧 How to Use

1. **Edit the script:**
   - Set the `TARGET_URL` variable to your target endpoint.
   - Example: `"https://target.site/dog?filename="`

2. **Run the script:**
```bash
python3 lfi_fuzzer.py
