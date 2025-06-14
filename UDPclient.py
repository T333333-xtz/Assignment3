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
    try:
        with open(file_list, 'r') as f:
            for line in f:
                file_name = line.strip()
                print(f"Downloading {file_name}...")
                download_message = f'DOWNLOAD {file_name}'
                response = sendAndReceive(sock, server_address, download_message)

                if response:
                    parts = response.split(" ")
                    if parts[0] == 'OK':
                        file_size = int(parts[3])
                        new_port = int(parts[5])
                        new_server_address = (hostname, new_port)

                        with open(file_name, 'wb') as output_file:
                            block_size = 1000
                            for start in range(0, file_size, block_size):
                                end = min(start + block_size - 1, file_size - 1)
                                file_request = f'FILE {file_name} GETSTART {start} END {end}'
                                data_response = sendAndReceive(sock, new_server_address, file_request)

                                if data_response:
                                    data_parts = data_response.split(" DATA ")
                                    if len(data_parts) > 1:
                                        base64Data = data_parts[1].strip()
                                        fileData = base64.b64decode(base64Data)
                                        output_file.seek(start)
                                        output_file.write(fileData)
                                        print("*", end="", flush=True)
                            close_message = f'FILE {file_name} CLOSE'
                            close_response = sendAndReceive(sock, new_server_address, close_message)
                            if close_response and close_response.startswith(f'FILE {file_name} CLOSE_OK'):
                                print(f"\nDownload of {file_name} completed.")
                    elif parts[0] == 'ERR':
                        print(f"Error: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
