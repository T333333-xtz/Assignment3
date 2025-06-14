import socket
import base64
import time

def sendAndReceive(sock, server_address, message, max_retries=5, initial_timeout=1):
    retries = 0
    timeout = initial_timeout
    while retries < max_retries:
        try:
            sock.settimeout(timeout)
            sock.sendto(message.encode(), server_address)
            data, server = sock.recvfrom(4096)
            return data.decode().strip()
        except socket.timeout:
            retries += 1
            timeout *= 2
            print(f"Timeout. Retrying ({retries}/{max_retries})...")
    print("Max retries reached. Giving up.")
    return None
