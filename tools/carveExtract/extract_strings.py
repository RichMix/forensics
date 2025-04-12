
def extract_strings(file_path, min_length=4):
    with open(file_path, "rb") as f:
        data = f.read()
    result = []
    current = b""
    for b in data:
        if 32 <= b <= 126:
            current += bytes([b])
        else:
            if len(current) >= min_length:
                result.append(current.decode("ascii", errors="ignore"))
            current = b""
    if len(current) >= min_length:
        result.append(current.decode("ascii", errors="ignore"))
    return result
