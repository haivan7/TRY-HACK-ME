<?php
// Hàm tính seed value từ email và constant_value
function calculate_seed_value($email, $constant_value) {
    $email_length = strlen($email); // Độ dài của email
    $email_hex = hexdec(substr($email, 0, 8)); // Chuyển đổi một phần email thành giá trị hex
    $seed_value = hexdec($email_length + $constant_value + $email_hex); // Tính toán giá trị seed

    return $seed_value;
}

// Nhận email từ đầu vào người dùng
echo "Nhập email của bạn: ";
$email = trim(fgets(STDIN)); // Lấy email từ người dùng

// Xác định constant_value
$constant_value = 99999; // Bạn có thể thay đổi giá trị này

// Gọi hàm calculate_seed_value để tạo seed value
$seed_value = calculate_seed_value($email, $constant_value);

// Sử dụng seed value để tạo mã invite code
mt_srand($seed_value);
$random = mt_rand();
$invite_code = base64_encode($random);

// In ra invite code
echo "Mã invite code của bạn: " . $invite_code . "\n";
?>
