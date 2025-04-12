# 🕵️‍♂️ Email Signature Analyzer – V2

This script scans a directory of PGP-signed email files to identify anomalies including:

- ✍️ Messages that are **not signed** by the expected entity (Liber8tion)
- ⚠️ Messages that have been **tampered with** (signature mismatch)
- 🧑‍💻 Messages that are signed by **unauthorized users**
- 🔐 Messages containing encoded payloads (Hex/Base64/ROT) that are auto-decoded

## 🧪 Detection Goals

| Question | Description |
|----------|-------------|
| Q1       | Filename of tampered message |
| Q2       | Plaintext of encoded message inside the tampered file |
| Q3       | Filename of message **not signed** by Liber8tion (even if signed by someone else) |
| Q4       | Email of the **unauthorized signer** |

---

## 🧰 How to Use

```bash
chmod +x analyze_emails_v2.sh
./analyze_emails_v2.sh
```

Ensure GPG is installed and accessible on your system.

---

## 🔑 Directory Requirements

- `~/pub_keys/`: Must contain public keys (e.g., `email_pub_key.asc`, `Dom_pub_key.asc`)
- `~/messages/`: Must contain message files `email_*.txt` and optional `.sig` signature files

---

## 🧩 Supported Encodings

- Hexadecimal strings (e.g., `4b767470`)
- Base64 strings (e.g., `U29tZXRleHQ=`)
- ROT-n ciphers (1 pass, auto-detect ROT-1 to ROT-25)

---

## 📄 Output

- Console output showing anomalies
- Decoded payload from tampered file (if possible)
