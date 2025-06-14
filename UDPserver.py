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
