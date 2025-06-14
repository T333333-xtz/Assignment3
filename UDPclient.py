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
    
def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 UDPclient.py <hostname> <port> <filename>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    file_list = sys.argv[3]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (hostname, port)
