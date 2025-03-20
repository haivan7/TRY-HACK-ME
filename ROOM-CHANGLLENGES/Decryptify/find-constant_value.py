import base64
import random
import hashlib

def calculate_seed_value(email, constant_value):
    # Lấy độ dài của email
    email_length = len(email)
    # Chuyển đổi 8 ký tự đầu tiên của email thành giá trị thập lục phân (hex)
    email_hex = int(hashlib.md5(email.encode()).hexdigest()[:8], 16)
    # Tính toán seed value
    seed_value = email_length + constant_value + email_hex
    return seed_value

def decode_invite_code(invite_code):
    # Giải mã base64
    decoded_bytes = base64.b64decode(invite_code)
    # Chuyển đổi từ bytes thành số nguyên
    random_value = int.from_bytes(decoded_bytes, 'big')
    return random_value

def find_constant_value(email, invite_code):
    random_value = decode_invite_code(invite_code)
    email_length = len(email)
    email_hex = int(hashlib.md5(email.encode()).hexdigest()[:8], 16)

    # Duyệt qua các giá trị constant_value để tìm
    for constant_value in range(1000000000):  # Thử với các giá trị từ 0 đến 100000
        seed_value = calculate_seed_value(email, constant_value)
        random.seed(seed_value)
        if random.randint(0, 2**32 - 1) == random_value:
            return constant_value

    return None

# Email và invite code đã cho
email = "alpha@fake.thm"
invite_code = "MTM0ODMzNzEyMg=="

# Tìm constant_value
constant_value = find_constant_value(email, invite_code)
if constant_value is not None:
    print("constant_value tìm được là:", constant_value)
else:
    print("Không tìm được constant_value phù hợp.")
