import os
import socket

KEEP_CONNECTION = True
HOST = "127.0.0.1"
PORT = 2546
BUFFER_SIZE = 4096


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"server in ascolto sulla porta {PORT}")

        while True:
            client_socket, client_addr = s.accept()
            print(f"Connessione accettata con {client_addr}")
            
            file_data = b""
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if len(data) == 0:
                    break
                file_data += data
            
            with open("keylogger.txt",'wb') as f:
                f.write(file_data)



if __name__ == "__main__":
    start_server()