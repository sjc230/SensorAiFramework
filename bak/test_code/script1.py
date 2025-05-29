import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

global server_socket

def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

def accept_connection():
    global client_socket, client_address
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    return client_socket

def close_server():
     server_socket.close()
     print("Server closed")

if __name__ == "__main__":
    start_server()
    try:
        client_socket = accept_connection()
        # Handle communication with the client using client_socket
    finally:
        close_server()