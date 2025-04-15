#!/bin/bash

TARGET="liber8login.web.cityinthe.cloud"
OUTDIR="recon_${TARGET}_$(date +%F_%H-%M-%S)"
mkdir "$OUTDIR"

echo "[*] Starting Nmap scan (full + service detection)..."
nmap -A -T4 "$TARGET" -oN "$OUTDIR/nmap_full.txt"

echo "[*] Running quick Nmap scan for common web ports..."
nmap -p 80,443,3000,3001,8000,8080,8443 -sV -Pn "$TARGET" -oN "$OUTDIR/nmap_webports.txt"

echo "[*] Running DIG queries..."
dig "$TARGET" +noall +answer > "$OUTDIR/dig_A.txt"
dig NS "$TARGET" +noall +answer > "$OUTDIR/dig_NS.txt"
dig MX "$TARGET" +noall +answer > "$OUTDIR/dig_MX.txt"

echo "[*] Attempting zone transfer (AXFR)..."
dig AXFR "$TARGET" @ns1."$TARGET" > "$OUTDIR/dig_AXFR.txt"

echo "[*] Running WHOIS (may return info for parent domain)..."
whois "$TARGET" > "$OUTDIR/whois.txt"

echo "[+] Recon complete. Output saved to: $OUTDIR"
