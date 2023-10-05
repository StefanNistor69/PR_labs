import socket
import signal
import sys
import threading
import json

HOST = '127.0.0.1'
PORT = 8080
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")


products = [
    {
        "name": "Fluent Python: Clear, Concise, and Effective Programming",
        "author": "Luciano Ramalho",
        "price": 39.95,
        "description": "Don't waste time bending Python to fit patterns you've learned in other languages..."
    },
    {
        "name": "Introducing Python: Modern Computing in Simple Packages",
        "author": "Bill Lubanovic",
        "price": 27.49,
        "description": "Easy to understand and fun to read..."
    }
]

def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]
    response_content = ''
    status_code = 200

    if path == '/':
        response_content = 'Home Page'
    elif path == '/about':
        response_content = 'About Us Page'
    elif path == '/contacts':
        response_content = 'Contacts Page'
    elif path == '/products':
        response_content = json.dumps(products)
    elif path.startswith('/product/'):
        product_id = int(path.split('/')[-1])
        if 0 <= product_id < len(products):
            response_content = json.dumps(products[product_id])
        else:
            response_content = 'Product not found'
            status_code = 404
    else:
        response_content = '404 Not Found'
        status_code = 404

    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()

