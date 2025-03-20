import sys                                                 
import socket                                              
import time                                                                                                           
import re                                                  
                                                                                         
def connect_to_port(host, port):
    try:                                               
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)  # Đặt thời gian chờ 4 giây                             
            s.connect((host, port))                    
            request = f'GET / HTTP/1.1\r\nHost: {host}\r\n\r\n'.encode('utf-8')      
            s.sendall(request)                         
            response = s.recv(1024).decode('utf-8')                                                                                         
            header, _, response = response.partition('\r\n\r\n')                                                  
            return response  # Trả về phần nội dung                                                            
                                                                                                                      
    except (socket.timeout, ConnectionRefusedError) as e:                                                          
        print(f"Error connecting to port {port}:{e}")
        return None                                
                                                                                         
                                                           
def parse_initial_response(response):                      
    print(f"Full response: {response}")                    
    match = re.search(r'onPort">(\d+)</a>', response)                                    
    if match:                                              
        next_port = int(match.group(1))                    
        return next_port                                   
    return None                                            
                                                                                         
                                                           
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
            print("Division by zero. Skipping divide")                                  
            return None, None                                                                                         
    return number, next_port                                                             
                                                                                                                      
def main():                                                                                                           
    host = '10.10.216.50'                                  
    port = 3010                                                                                                       
    number = 0                                             
    retries = 30   # Đặt số lần thử lại
    delay = 0.2  # Khoảng thời gian chờ giữa mỗi lần thử lại

    # Thử kết nối với port 3010, với số lần thử lại là 15 lần
    response = None
    for attempt in range(retries):
        response = connect_to_port(host, port)
        if response:
            break
        else:
            print(f"Failed to connect to port 3010 on attempt {attempt + 1}/{retries}. Retrying in {delay} seconds...")
            time.sleep(delay)
    
    if not response:  # Nếu không kết nối được sau retries lần
        print(f"Failed to connect to initial port 3010 after {retries} attempts.")
        return
    
    # Xử lý phản hồi từ port 3010
    next_port = parse_initial_response(response)
    if not next_port:                                       
        print("Failed to extract port from initial response")                                                      
        return

    print(f"Next port: {next_port}")

    # Thực hiện kết nối với các port tiếp theo cho đến khi gặp port 9765 hoặc lệnh STOP
    while next_port and next_port != 9765:                                                                             
        time.sleep(0.5)
        
        # Thử lại kết nối với các port tiếp theo trong trường hợp thất bại (với số lần retries)
        response = None
        for attempt in range(retries):
            response = connect_to_port(host, next_port)
            if response:
                break
            else:
                print(f"Failed to connect to port {next_port} on attempt {attempt + 1}/{retries}. Retrying in {delay} seconds...")
                time.sleep(delay)
        
        if not response:  # Nếu không kết nối được sau retries lần
            print(f"Failed to connect to port {next_port} after {retries} attempts.")
            break
        
        # Xử lý phản hồi từ port tiếp theo
        print(f"Response from port {next_port}: {response}")
        number, next_port = parse_operation_response(response, number)
        if next_port is None:                                                                                      
            print("STOP received or invalid response. Stopping.")                                                   
            break                                                                                                  
        print(f"Current number: {number}, Next port: {next_port}")                                                 
        print("-------------------------------------------------")


                                                                                                                      
if __name__ == "__main__":                                                                                             
    main() 
