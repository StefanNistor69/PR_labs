import socket

def tcp_client_request(path):
    HOST = '127.0.0.1'
    PORT = 8080
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    request = f"GET {path} HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(4096).decode('utf-8')
    print(response)
    client_socket.close()


tcp_client_request('/')
tcp_client_request('/about')
tcp_client_request('/contacts')
tcp_client_request('/products')
tcp_client_request('/product/0')
tcp_client_request('/product/1')
tcp_client_request('/nonexistent')
