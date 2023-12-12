import socket

def start_server(port=9355):
    host = '0.0.0.0'  # Localhost

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    # set reuse
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  

    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    return server_socket
        
def accept_client(server_socket):
    client_socket, addr = server_socket.accept()
    print("Received connection from ", addr)
    return client_socket

if __name__ == "__main__":
    start_server()