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
