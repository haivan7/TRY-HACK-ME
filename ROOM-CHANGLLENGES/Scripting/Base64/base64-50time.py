#!/usr/bin/python3

import base64

input_file=input("Enter file path:")

with open(input_file,"r") as file:
    content = file.read()


def decode_base64(content):
    for i in range(50):
        try:

            content = base64.b64decode(content).decode("utf-8")
        except Exception as e:
            print("Error decoding at iteraction {i+1}: {e}")
            break
        
    return  content


decoded_content = decode_base64(content)
print(decoded_content)
