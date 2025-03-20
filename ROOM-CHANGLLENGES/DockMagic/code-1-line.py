def process_file_to_one_line(input_file, output_file):
    with open(input_file, 'r') as file:
        # Read the file and remove newlines and spaces to form a single line
        content = file.read().replace('\n', '').replace(' ', '')
        
    # Write the processed content to the output file
    with open(output_file, 'w') as file:
        file.write(content)
        
    return content

# Example usage with new file paths
input_file_path = '/home/sherlock-parrot/THM/ROOM-CHANGLLENGES/DockMagic/encode-ssh-key.txt'
output_file_path = '/home/sherlock-parrot/THM/ROOM-CHANGLLENGES/DockMagic/ssh-key-1-line.txt'
processed_content = process_file_to_one_line(input_file_path, output_file_path)

processed_content  # Return the single-line output content
