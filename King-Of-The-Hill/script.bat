powershell -c "Invoke-WebRequest -Uri http://127.0.0.1:9999/king.txt -OutFile 'C:\Shares\King\king.txt'"
echo  has king! %USERNAME% queried king.txt at %DATE% %TIME% >> C:\Shares\King\king.txt
