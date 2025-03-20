#!/usr/bin/bash

read -p "Enter file path to decode:" input_file

if [[ ! -f "$input_file" ]]; then
    echo "ERROR : File not found!"
    exit 1
fi

content=$(cat "$input_file")

trap 'echo "Error : Decoding failed at $i"; exit 1' ERR

for i in {1..50}; do 
    content=$(echo "$content" | base64 --decode 2>/dev/null)
    if [[ $? -ne 0 ]]; then
        echo "Error : failed in $i. Error message : $(echo $content | base64 --decode 2>&1)"
        exit 1
    fi
done

echo "$content"


