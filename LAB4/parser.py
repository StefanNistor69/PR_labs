import socket
import json

HOST = '127.0.0.1'
PORT = 8080


def tcp_client_request(path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    request = f"GET {path} HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(4096).decode('utf-8')
    client_socket.close()
    return response


def parse_response(response):
    headers, content = response.split('\n\n', 1)
    return content


def get_all_pages():
    pages = {
        '/': 'Home Page',
        '/about': 'About Us Page',
        '/contacts': 'Contacts Page'
    }


    products_response = tcp_client_request('/products')
    products_content = parse_response(products_response)
    products_list = json.loads(products_content)

    for idx, product in enumerate(products_list):
        product_path = f'/product/{idx}'
        product_response = tcp_client_request(product_path)
        product_content = parse_response(product_response)
        product_details = json.loads(product_content)
        pages[product_path] = product_details

    return pages


pages_content = get_all_pages()
for path, content in pages_content.items():
    print(f"Path: {path}")
    print(f"Content: {content}")
    print("===================================")
