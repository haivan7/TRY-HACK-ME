#!/usr/bin/python3

import socket
import re
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Thông tin server
server_ip = "10.10.24.84"
server_port = 4000
server_address = (server_ip, server_port)

# Tạo socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Already connected to server ip {server_ip}:{server_port}")
print("-----------")

# Gửi tin nhắn 'hello' để nhận thông tin ban đầu
sock.sendto(b'hello', server_address)
data, _ = sock.recvfrom(1024)
data_str = data.decode()
print(f"Response after sending message 'hello': {data_str}")
print("-----------")

# Gửi tin nhắn 'ready' để nhận thêm thông tin
sock.sendto(b'ready', server_address)
data, _ = sock.recvfrom(1024)
data_str = data.decode('latin1')
print(f"Response after sending message 'ready': {data_str}")
print("-----------")

# Extract key, iv và checksum từ phản hồi
key = re.search(r'key:(\S+)', data_str).group(1)
iv = re.search(r'iv:(\S+)', data_str).group(1)
checksum = re.search(rb'SHA256 checksum of (.+?) send', data).group(1)

print(f"Key: {key}")
print(f"IV: {iv}")
print(f"Checksum: {checksum}")
print("-----------")

# Gửi tin nhắn 'final' để nhận dữ liệu được mã hóa
sock.sendto(b'final', server_address)
enc_data, _ = sock.recvfrom(1024)
print(f"Received encrypted data (in bytes): {enc_data}")
print("-----------")

# Chuyển đổi key và iv từ chuỗi sang bytes
key_bytes = key.encode('utf-8')
iv_bytes = iv.encode('utf-8')

# Giả sử server gửi encrypted_data và tag nối tiếp nhau
# AES-GCM cần cả encrypted_data và tag để giải mã
encrypted_text = enc_data[:-16]  # Giả sử tag dài 16 bytes (128 bit)
tag = enc_data[-16:]

# Tạo AES-GCM cipher object
aesgcm = AESGCM(key_bytes)

# Giải mã dữ liệu
try:
    decrypted_data = aesgcm.decrypt(iv_bytes, encrypted_text + tag, None)
    print(f"Decrypted data: {decrypted_data}")

    # Tính toán checksum SHA256 của dữ liệu giải mã
    calculated_checksum = hashlib.sha256(decrypted_data).digest()
    print(f"Calculated checksum: {calculated_checksum}")

    # So sánh checksum nhận được với checksum từ server
    if calculated_checksum == checksum:
        print("Checksums match! The flag is valid.")
    else:
        print("Checksums do not match. Something went wrong.")

except Exception as e:
    print(f"An error occurred during decryption: {e}")
