import socket

AMAZON_HOST = "0.0.0.0"
AMAZON_PORT = 6543

amazon_ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
amazon_ups_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
amazon_ups_socket.bind((AMAZON_HOST, AMAZON_PORT))

print(f"Successfully bound to {AMAZON_HOST}:{AMAZON_PORT}")