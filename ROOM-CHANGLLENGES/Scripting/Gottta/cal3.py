import sys                                                 
import socket                                              
import time                                                                                                           
import re

# Hàm để kết nối đến một cổng với giới hạn số lần thử
def connect_to_port(host, port, retries=3, delay=0.5):                                   
    for attempt in range(retries):                         
        try:                                               
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:                                              
                s.settimeout(4)  # Đặt thời gian chờ 4 giây                             
                s.connect((host, port))                    
                request = f'GET / HTTP/1.1\r\nHost: {host}\r\n\r\n'.encode('utf-8')      
                s.sendall(request)                         
                response = s.recv(1024).decode('utf-8')                                  
                                                                                         
                header, _, response = response.partition('\r\n\r\n')                                                  
                return response  # Chỉ trả về phần nội dung                                                                                              
        except (socket.timeout, ConnectionRefusedError) as e:                                                          
            print(f"Error connecting to port {port}: {e}")                                                             
            if attempt < retries - 1:                      
                print(f"Retrying in {delay} seconds...")                                                               
                time.sleep(delay)                                                        
            else:                                          
                print(f"Failed to connect after {retries} attempts")                                                   
                return None                                

# Hàm để phân tích phản hồi ban đầu và tìm cổng tiếp theo
def parse_initial_response(response):                      
    print(f"Full response: {response}")                    
    match = re.search(r'onPort">(\d+)</a>', response)                                    
    if match:                                              
        next_port = int(match.group(1))                    
        return next_port                                   
    return None                                            

# Hàm phân tích phản hồi và thực hiện phép tính
def parse_operation_response(response, number):                                                                         
    if not response:                                       
        print("Received an empty response or no data from the server")                                                  
        return None, None                                  
    if 'STOP' in response:                                                                                            
        print("STOP command received")                      
        return None, None                                  
                                                                                         
    parts = response.split()                               
    if len(parts) < 3:                                                                   
        return None, None                                  
                                                                                         
    operation = parts[0]                                                                 
    value = int(parts[1])                                                                
    next_port = int(parts[2])                              
                                                                                                                      
    if operation == 'add':                                 
        number += value                                                                                               
    elif operation == 'minus':                             
        number -= value                                                                                               
    elif operation == 'multiply':                          
        number *= value                                                                  
    elif operation == 'divide':                            
        if value != 0:                                                                                                
            number //= value                                                             
        else:                                              
            print("Division by zero . Skipping divide")                                  
            return None, None                                                                                         
    return number, next_port                                                             

def main():                                                                                                           
    host = '10.10.216.50'                                  
    port = 3010                                                                                                       
    number = 0                                             
    break_times = 15  # Số lần thử kết nối tối đa
    tries = 0  # Biến đếm số lần thử kết nối
    
    # Kết nối lần đầu tiên
    response = connect_to_port(host, port)                  
    if response:                                                                                                      
        next_port = parse_initial_response(response)                                                                   
        if next_port:                                      
            print(f"Next port: {next_port}")                                                                           
        else:                                                                                                                                                                                                                                                                                                                                                       
            print("Failed to extract port from initial response")                                                      
            return                                                                                                     
    else:                                                                                                              
        print(f"Full response: {response}")                                                                             
        print("Failed to connect to initial port 3010")                                                                
        return                                                                                                         
    
    # Vòng lặp chính để kết nối qua các cổng
    while next_port and next_port != 9765 and tries < break_times:                                                                             
        time.sleep(0.5)  # Delay giữa các lần kết nối
        response = connect_to_port(host, next_port)                                                                     
        if response:                                                                                                   
            print(f"Response from port {next_port}: {response}")                                                        
            number, next_port = parse_operation_response(response, number)                                             
            if next_port is None:                                                                                      
                print("STOP received or invalid response, stopping")                                                   
                break                                                                                                  
            print(f"Current number: {number}, Next port: {next_port}")                                                 
        else:                                                                                                          
            tries += 1  # Tăng số lần thử kết nối lên
            print(f"Failed to get a response from the next port: {next_port}. Attempt {tries}/{break_times}")
            if tries == break_times:
                print("Reached maximum retry limit, stopping.")
                break

if __name__ == "__main__":                                                                                             
    main()   
