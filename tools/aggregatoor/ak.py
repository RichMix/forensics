#!/bin/bash

# === Configuration ===
MESSAGE_DIR=~/messages
KEY_DIR=~/pub_keys

echo "🛠️  Importing Public Keys..."
gpg --import "$KEY_DIR"/*.asc > /dev/null 2>&1

echo "🔍 Scanning messages in $MESSAGE_DIR..."
cd "$MESSAGE_DIR" || exit

# === Q3: Find message that was not signed ===
echo -e "\n📭 Messages without signature:"
for f in email_*.txt; do
    if [ ! -f "${f}.sig" ]; then
        echo "Unsigned: $f"
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
            SIGNER=$(echo "$OUT" | grep "Good signature" | sed 's/.*user //')
            if ! echo "$SIGNER" | grep -qi "liber8tion"; then
                echo "⚠️  Unexpected signer for $f: $SIGNER"
                FOREIGN_SIGNED_FILE="$f"
                FOREIGN_SIGNER="$SIGNER"
            fi
        else
            echo "❓ Unknown verification result for $f"
        fi
    fi
done

# === Q2: Decode message in tampered file ===
if [ -n "$TAMPERED_FILE" ]; then
    echo -e "\n🔓 Attempting to decode tampered message in $TAMPERED_FILE..."
    TAIL=$(tail -n 1 "$TAMPERED_FILE")

    if [[ "$TAIL" =~ ^[A-Fa-f0-9]+$ ]]; then
        echo "Detected Hex. Decoding..."
        echo "$TAIL" | xxd -r -p
    elif [[ "$TAIL" =~ ^[A-Za-z0-9+/=]+$ ]]; then
        echo "Detected Base64. Decoding..."
        echo "$TAIL" | base64 -d
    else
        echo "Unrecognized encoding or plaintext: $TAIL"
    fi
fi

# === Summary ===
echo -e "\n📋 Summary:"
[ -n "$TAMPERED_FILE" ] && echo "Q1) Tampered file: $TAMPERED_FILE"
[ -n "$TAIL" ] && echo "Q2) Last line (possibly encoded message): $TAIL"
[ -n "$UNSIGNED_FILE" ] && echo "Q3) Unsigned file: $UNSIGNED_FILE"
[ -n "$FOREIGN_SIGNED_FILE" ] && echo "Q4) Non-Liber8tion-signed file: $FOREIGN_SIGNED_FILE"
[ -n "$FOREIGN_SIGNER" ] && echo "    Signed by: $FOREIGN_SIGNER"

echo -e "\n✅ Done!"
