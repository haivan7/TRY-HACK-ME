import hmac
import hashlib

message = b'smashthestate'  # Chuỗi gốc dạng byte
key = b'jlebedev'           # Key (username của JL)
hmac_obj = hmac.new(key, message, hashlib.md5)
hash_result = hmac_obj.hexdigest()  # Kết quả dạng hex
vnc_password = hash_result[:8]      # Lấy 8 ký tự đầu

print("Full HMAC-MD5 hash:", hash_result)
print("VNC password:", vnc_password)
