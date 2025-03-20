import random
import base64

# Hàm tính giá trị seed dựa trên email và giá trị hằng số
def calculate_seed_value(email, constant_value):
    email_length = len(email)
    email_hex = int(email[:8].encode('utf-8').hex(), 16)
    seed_value = email_length + constant_value + email_hex
    return seed_value

# Hàm tạo mã mời (invite code)
def generate_invite_code(email, constant_value):
    seed_value = calculate_seed_value(email, constant_value)
    random.seed(seed_value)  # Khởi tạo random bằng giá trị seed
    random_number = random.randint(0, 2**32 - 1)  # Sinh số ngẫu nhiên
    invite_code = base64.b64encode(str(random_number).encode('utf-8')).decode('utf-8')
    return invite_code

# Ví dụ đầu vào
email = "alpha@fake.thm"
constant_value = 999999

invite_code = generate_invite_code(email, constant_value)
print(f"{invite_code}")
