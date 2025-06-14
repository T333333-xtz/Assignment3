import socket
import threading
import base64
import random
import os

def handleFileTransmission(file_name, client_address):
    # 选择一个随机端口号
    new_port = random.randint(50000, 51000)
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_socket.bind(('0.0.0.0', new_port))

try:
        file_size = os.path.getsize(file_name)
        response = f'OK {file_name} SIZE {file_size} PORT {new_port}'
        new_socket.sendto(response.encode(), client_address)
 with open(file_name, 'rb') as file:
            while True:
                data, client = new_socket.recvfrom(1024)
                client_request = data.decode().strip()
                parts = client_request.split(" ")

                if parts[0] == 'FILE' and parts[3] == 'CLOSE':
                    close_response = f'FILE {file_name} CLOSE_OK'
                    new_socket.sendto(close_response.encode(), client)
                    break

                elif parts[0] == 'FILE' and parts[3] == 'GETSTART':
                    start = int(parts[4])
                    end = int(parts[6])
                    file.seek(start)
                    actual_bytes = file.read(end - start + 1)
                    base64Data = base64.b64encode(actual_bytes).decode()
                    response = f'FILE {file_name} OK START {start} END {end} DATA {base64Data}'
                    new_socket.sendto(response.encode(), client)
    except Exception as e:
        print(f"Error handling file transmission: {e}")
    finally:
        new_socket.close()
        
def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 UDPserver.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    welcome_socket.bind(('0.0.0.0', port))

    print(f"Server is listening on port {port}")
    
    while True:
        data, client_address = welcome_socket.recvfrom(1024)
        client_request = data.decode().strip()
        parts = client_request.split(" ")

        if parts[0] == 'DOWNLOAD':
            file_name = parts[1]
            if os.path.exists(file_name):
                # 创建新线程处理文件传输
                threading.Thread(target=handleFileTransmission, args=(file_name, client_address)).start()
            else:
                error_response = f'ERR {file_name} NOT_FOUND'
                welcome_socket.sendto(error_response.encode(), client_address)
if __name__ == "__main__":
    main()
