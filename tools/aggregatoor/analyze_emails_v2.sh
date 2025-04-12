#!/bin/bash

# === CONFIG ===
MESSAGE_DIR=~/messages
KEY_DIR=~/pub_keys
EXPECTED_DOMAIN="liber8tion"

echo "🛠️  Importing Public Keys..."
gpg --import "$KEY_DIR"/*.asc > /dev/null 2>&1

echo "🔍 Scanning messages in $MESSAGE_DIR..."
cd "$MESSAGE_DIR" || exit

# === Trackers ===
UNSIGNED_FILE=""
TAMPERED_FILE=""
FOREIGN_SIGNED_FILE=""
FOREIGN_SIGNER=""
TAMPERED_PAYLOAD=""
DECODED_PAYLOAD=""

# === Q3: Find message that was not signed ===
echo -e "\n📭 Messages without signature:"
for f in email_*.txt; do
    if [ ! -f "${f}.sig" ]; then
        echo "❌ Unsigned: $f"
        UNSIGNED_FILE="$f"
    fi
done

# === Q1 & Q4: Check for tampered or foreign-signed messages ===
echo -e "\n🔏 Verifying signatures..."
for f in email_*.txt; do
    SIG="${f}.sig"
    if [ -f "$SIG" ]; then
        OUT=$(gpg --verify "$SIG" "$f" 2>&1)
        if echo "$OUT" | grep -q "BAD signature"; then
            echo "❌ Tampered: $f"
            TAMPERED_FILE="$f"
        elif echo "$OUT" | grep -q "Good signature"; then
            SIGNER=$(echo "$OUT" | grep "Good signature" | sed 's/.*Good signature from //')
            if ! echo "$SIGNER" | grep -qi "$EXPECTED_DOMAIN"; then
                echo "⚠️  Non-Liber8tion signer for $f: $SIGNER"
                FOREIGN_SIGNED_FILE="$f"
                FOREIGN_SIGNER="$SIGNER"
                UNSIGNED_FILE="$f"
            fi
        fi
    fi
done

# === Q2: Decode message in tampered file ===
if [ -n "$TAMPERED_FILE" ]; then
    echo -e "\n🔓 Attempting to decode payload in $TAMPERED_FILE..."
    TAIL=$(tail -n 1 "$TAMPERED_FILE")
    TAMPERED_PAYLOAD="$TAIL"

    if [[ "$TAIL" =~ ^[A-Fa-f0-9]+$ ]]; then
        echo "🧪 Detected Hex. Decoding..."
        DECODED_PAYLOAD=$(echo "$TAIL" | xxd -r -p)
    elif [[ "$TAIL" =~ ^[A-Za-z0-9+/=]+$ ]]; then
        echo "🧪 Detected Base64. Decoding..."
        DECODED_PAYLOAD=$(echo "$TAIL" | base64 -d 2>/dev/null)
    else
        echo "🧪 Unknown encoding. Trying ROT bruteforce..."
        for i in {1..25}; do
            ROTTRY=$(echo "$TAIL" | tr 'A-Za-z' "$(echo {A..Z} {A..Z} | cut -d' ' -f$((i+1))-26,$((i)) | tr -d ' ')""$(echo {a..z} {a..z} | cut -d' ' -f$((i+1))-26,$((i)) | tr -d ' ')")
            if echo "$ROTTRY" | grep -qE '[Dd]omin8tion'; then
                echo "✔️  Detected ROT-$i: $ROTTRY"
                DECODED_PAYLOAD="$ROTTRY"
                break
            fi
        done
    fi
fi

# === Summary ===
echo -e "\n📋 Summary:"
[ -n "$TAMPERED_FILE" ] && echo "Q1) Tampered file: $TAMPERED_FILE"
[ -n "$TAMPERED_PAYLOAD" ] && echo "Q2) Encoded: $TAMPERED_PAYLOAD"
[ -n "$DECODED_PAYLOAD" ] && echo "    Decoded: $DECODED_PAYLOAD"
[ -n "$UNSIGNED_FILE" ] && echo "Q3) Not signed by Liber8tion: $UNSIGNED_FILE"
[ -n "$FOREIGN_SIGNER" ] && echo "Q4) Signed by: $FOREIGN_SIGNER"

echo -e "\n✅ Done!"
