
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
PNG_FOOTER = b"\x00\x00\x00\x00IEND\xaeB\x60\x82"

with open("challenge.img", "rb") as f:
    img_data = f.read()

start_index = img_data.find(PNG_HEADER)
end_index = img_data.find(PNG_FOOTER, start_index)
if start_index != -1 and end_index != -1:
    end_index += len(PNG_FOOTER)
    carved_png = img_data[start_index:end_index]
    with open("recovered_super_secret_flag5834.png", "wb") as out_file:
        out_file.write(carved_png)
