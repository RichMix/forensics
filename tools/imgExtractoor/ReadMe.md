🔧 How to Use the Script

python3 forensics_carver.py ForYou.jpg
It will carve and save:

All JPEGs (carved_jpeg_*.jpg)

All ZIPs (carved_zip_*.zip)

📖 Full Extraction & Write-Up (Terminal Style)
🔍 Step 1: Identify Hidden Content

strings ForYou.jpg | tail
Look for clues like embedded .txt or .jpg file names.

🧪 Step 2: Analyze with binwalk

sudo apt install binwalk
binwalk ForYou.jpg
Result shows ZIPs, JPEGs, or other headers.

📦 Step 3: Extract Files with binwalk

binwalk --extract ForYou.jpg
Creates a directory:

_ForYou.jpg.extracted/
Check contents:


ls -lh _ForYou.jpg.extracted/
🔁 Step 4: Manual Extraction (if needed)
If some files are still hidden:

Option A: Use Python Script

python3 forensics_carver.py ForYou.jpg
Option B: Grep JPEG headers

xxd ForYou.jpg | grep -a -obUaP '\xff\xd8\xff'
📚 Output Overview

File	Content
carved_zip_1.zip	Contains 4Congrats.txt, 6Bussin.txt
carved_jpeg_*.jpg	One of these held Q1 flag visually
