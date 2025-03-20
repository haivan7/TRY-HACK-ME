import socket
import re

HOST = "10.10.216.50"
PORT = 3010 
flag = 0
response = ""
times = 0
break_times = 15

print("--------------------------------------------------------")
while 1:
    try: 
        print(f"Connecting to {HOST} port {PORT} ...")
        # Tạo kết nối đến máy chủ
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
         
        # Tạo yêu cầu và gửi
        request = f"GET / HTTP/1.1\r\nHost:{HOST}\r\n\r\n"
        client.send(request.encode())
        
        # Nhận phản hồi
        response = client.recv(4096)
        print("status: collected data")
        response = response.split(b'\r\n\r\n')[1].decode()
        print("Filtered: ", response)
        print("Len: ", len(response))
        
        # Nếu response có nội dung
        if len(response) > 0:
            print("Let's change something") 
            
            # Kiểm tra nếu response chứa 'STOP' hoặc port bằng 9765
            if ("STOP" in response) or (PORT == 9765):
                times = break_times
                break
            
            # Xử lý nếu độ dài response bằng 1033
            if len(response) >= 1000:
                print("Found specific length response, trying to extract port.")
                match = re.search(r'onPort">(\d+)</a>', response)
                if match:
                    next_port = int(match.group(1))
                    print(f"Found next port: {next_port}")
                    PORT = next_port
                    times = 0  # Đặt lại số lần thử cho cổng mới
                    continue  # Tiếp tục với cổng mới mà không tăng 'times'
            
            # Tách phản hồi và xử lý toán tử
            cal = response.split()
            if len(cal) >= 3:
                print("Operation: ", cal[0])
                print("Num: ", float(cal[1]))
                
                # Chuyển đổi sang port mới nếu port thay đổi
                if int(cal[2]) != PORT:
                    times -= 3
                
                # Chuyển đến cổng tiếp theo
                print("Change port to: ", int(cal[2]))
                PORT = int(cal[2])
                
                # Tính toán giá trị cờ (flag)
                if cal[0] == "add":
                    flag += float(cal[1])
                elif cal[0] == "minus":
                    flag -= float(cal[1])
                elif cal[0] == "multiply":
                    flag *= float(cal[1])
                elif cal[0] == "divide":
                    flag /= float(cal[1])
                print("Current flag: ", flag)
            else:
                print("Unexpected response format: ", response)
        else:
            print("Empty response")
            
    except Exception as e:
        print(e)
        times += 1
        print(f"No connection :<\n{break_times-times} times left.")
    
    # Nếu số lần thử vượt quá giới hạn, kết thúc chương trình
    if times == break_times:
        break
    
    print("--------------------------------------------------------")

print("--------------------------------------------------------")
print(f"Flag : {flag:.2f}")
print("--------------------------------------------------------")
