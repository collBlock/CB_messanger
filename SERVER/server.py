import socket
import json
import time
import os


local_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (local_ip, 2000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(2)

# Wait for a connection
print('waiting for a connection')
connection1, client_address1 = sock.accept()
connection2, client_address2 = sock.accept()

print('connection from', client_address1, client_address2)

# Receive the data in small chunks and retransmit it
while True:
    try:
        data1 = connection1.recv(1024)
        data2 = connection2.recv(1024)
        if data1:
            print('{!r} from {}'.format(data1.decode(), client_address1))
            connection2.sendall(data1)
            # Store the data in a json file
            info = {
                'time': time.time(),
                'from': client_address1,
                'message': data1.decode()
            }
            
            with open('data.json', 'r+') as f:
                if os.stat('data.json').st_size == 0:
                    data = []
                else:
                    data = json.load(f)
                
                data[len(data)+1] = info
                f.seek(0)
                json.dump(data, f)
                f.truncate()
        
        if data2:
            print('received {!r} from {}'.format(data2.decode(), client_address2))
            connection1.sendall(data2)
            # Store the data in a json file
            info = {
                'time': time.time(),
                'from': client_address2,
                'message': data2.decode()
            }
            
            with open('data.json', 'r+') as f:
                if os.stat('data.json').st_size == 0:
                    data = []
                else:
                    data = json.load(f)
                
                data[len(data)+1] = info
                f.seek(0)
                json.dump(data, f)
                f.truncate()# Clean up the connection
    except:
        break
print('closing socket')
connection1.close()
connection2.close()
os.system('cls')