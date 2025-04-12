
import re
import sys

def extract_jpegs_and_zips(filename):
    with open(filename, "rb") as f:
        data = f.read()

    # Locate JPEG start markers (FFD8FF)
    jpeg_offsets = [m.start() for m in re.finditer(b'\xff\xd8\xff', data)]

    # Locate ZIP signatures (PK\x03\x04)
    zip_offsets = [m.start() for m in re.finditer(b'PK\x03\x04', data)]

    # Carve JPEGs
    for i in range(len(jpeg_offsets)):
        start = jpeg_offsets[i]
        end = jpeg_offsets[i+1] if i+1 < len(jpeg_offsets) else len(data)
        with open(f"carved_jpeg_{i+1}.jpg", "wb") as out:
            out.write(data[start:end])
        print(f"[+] Carved JPEG: carved_jpeg_{i+1}.jpg (offset: {hex(start)})")

    # Carve ZIPs
    for i in range(len(zip_offsets)):
        start = zip_offsets[i]
        end = zip_offsets[i+1] if i+1 < len(zip_offsets) else len(data)
        with open(f"carved_zip_{i+1}.zip", "wb") as out:
            out.write(data[start:end])
        print(f"[+] Carved ZIP: carved_zip_{i+1}.zip (offset: {hex(start)})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 forensics_carver.py <image_file>")
        sys.exit(1)
    extract_jpegs_and_zips(sys.argv[1])
