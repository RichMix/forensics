# 🧠 Full CTF Decoder v0.0.5

Version 5 brings full transposition cipher coverage and advanced decoding power for serious CTF challenges.

---

## ✨ New in V5 (Transposition Suite)

| Cipher Type                | Description                                         |
|----------------------------|-----------------------------------------------------|
| ✅ Columnar Transposition  | Reorders columns, supports brute-force + key        |
| ✅ Scytale Cipher          | Wraps around rod, simulates row-by-column unwrap    |
| ✅ Spiral/Route Cipher     | Reads characters in spiral matrix pattern           |
| ✅ Brute-force grid widths | Auto-trial matrix widths for transposition patterns |

---

## 🧩 All Cipher & Encoding Support (Full Suite)

### 🔁 Classic Ciphers
- Caesar (ROT1–25)
- ROT13
- ROT5 (numbers)
- Atbash
- Affine Cipher (planned)
- Vigenère Cipher (planned)

### 🔡 Encodings
- Binary
- Hex
- ASCII code (numeric)
- Base64

### 📡 Signal & Symbolic
- Morse
- Morse + ROTN combo
- Braille (planned)
- Tap code (planned)

### 🧱 Transposition
- Rail Fence (brute-force rails 2–10)
- Columnar Transposition
- Scytale Cipher
- Spiral Matrix (clockwise)

---

## 🛠 Usage

```bash
python3 full_ctf_decoder_v5.py --input "<your_encoded_string_here>"
```

This will run all decoders and show every likely match.

---

## 📌 Next Up (V6+ Ideas)

- 🧠 Frequency analysis & dictionary scoring
- 🌐 API integration for hash/crack stations
- 🧰 Visual matrix render (CLI or web)
- 🧮 XOR and AES brute-forcing (mini-crypto block)

---

Made by Chopp Sueyy & ChatGPT
CTF tools that slap 💥
