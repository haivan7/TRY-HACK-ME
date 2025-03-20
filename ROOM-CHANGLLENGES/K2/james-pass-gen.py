#!/usr/bin/env python3

import string

base_pass = "rockyou"
special_chars = string.punctuation

f = open("./james_possible_passwords.txt", "w")

for i in range(0, 10):
	for special_char in special_chars:
		f.write(f"{base_pass}{special_char}{i}\n")
		f.write(f"{base_pass}{i}{special_char}\n")
		f.write(f"{special_char}{i}{base_pass}\n")
		f.write(f"{i}{special_char}{base_pass}\n")
		f.write(f"{i}{base_pass}{special_char}\n")
		f.write(f"{special_char}{base_pass}{i}\n")

f.close()
