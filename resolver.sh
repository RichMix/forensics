#!/bin/bash

echo "[*] Brute-forcing DNS resolver on 10.4.194.0/27..."

# Step 1: Find working resolver
for i in $(seq 1 62); do
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
  echo "❌ Could not find a valid DNS resolver in subnet."
  exit 1
fi

echo -e "\n[*] Using resolver: $RESOLVER"
echo "-------------------------------"

# Step 2: Run all questions
echo -n "Q1 - IPv4 address for liber8.cityinthe.cloud: "
dig @$RESOLVER liber8.cityinthe.cloud A +short

echo -n "Q2 - IPv6 address for liber8.cityinthe.cloud: "
dig @$RESOLVER liber8.cityinthe.cloud AAAA +short

echo -n "Q3 - TXT flag at flag.liber8.cityinthe.cloud: "
dig @$RESOLVER flag.liber8.cityinthe.cloud TXT +short

echo -n "Q4 - CNAME redirect for redirect.liber8.cityinthe.cloud: "
CNAME_TARGET=$(dig @$RESOLVER redirect.liber8.cityinthe.cloud CNAME +short)
echo $CNAME_TARGET

echo -n "Q5 - TTL for redirect.liber8.cityinthe.cloud (in seconds): "
dig @$RESOLVER redirect.liber8.cityinthe.cloud CNAME | grep redirect | awk '{print $2}'

echo -n "Q6 - IPv4 for the redirected domain ($CNAME_TARGET): "
dig @$RESOLVER $CNAME_TARGET A +short

echo -n "Q7 - MX record (mail server) for mail.liber8.cityinthe.cloud: "
dig @$RESOLVER mail.liber8.cityinthe.cloud MX +short | sort -n | head -n1 | awk '{print $2}'
