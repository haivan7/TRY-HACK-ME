import socket

HOST = "10.10.216.50"
PORT = 3010 
flag = 0
response = ""
times = 0
operation = {}
break_times = 15

print("--------------------------------------------------------")
while 1:
    try: 
        print("Connecting to "+HOST+" port "+str(PORT)+" ...")
        #create connection to host
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
         
        # create request and sent it
        request = "GET / HTTP/1.1\r\nHost:"+HOST+"\r\n\r\n"
        client.send(request.encode())
        
        # get response
        response = client.recv(4096)
        print("status: collected data")
        response = response.split(b'\r\n\r\n')[1].decode()
        print("Filtered: ", response)
        print("Len: ", len(response))
        
        if len(response) > 0:
            print("Let\'s change somethin'") 
            #STOP point
            if ("STOP" in response) or (PORT == 9765):
                times = break_times
                break
            
            # Split response and validate length
            cal = response.split()
            if len(cal) >= 3:
                print("Operation: ", cal[0])
                print("Num: ", float(cal[1]))
                #improve for changing port 
                if int(cal[2]) != PORT:
                    times -= 3
                #Change to next port
                print("Change port to: ", int(cal[2]))
                PORT = int(cal[2])
                
                #calculate flag
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
        print("No connection :<")
        print(str(break_times-times)+" times left. ")
    
    if  times == break_times:
        break
    
    print("--------------------------------------------------------")

print("--------------------------------------------------------")
print("Flag : %.2f" % flag)
print("--------------------------------------------------------")
