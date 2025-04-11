#!/bin/bash
echo "[*] Brute-forcing DNS resolver on 10.4.194.0/24..."
for i in $(seq 1 254); do
  echo -n "Trying 10.4.194.$i ... "
  result=$(dig @10.4.194.$i liber8.cityinthe.cloud A +short +time=1 +tries=1 2>/dev/null)
  if [[ "$result" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "✅ SUCCESS: $result"
    RESOLVER="10.4.194.$i"
    break
  else
    echo "No response"
  fi
done
if [[ -z "$RESOLVER" ]]; then
  echo "❌ Could not find a valid DNS resolver."
else
  echo "[*] Resolver found: $RESOLVER"
fi
