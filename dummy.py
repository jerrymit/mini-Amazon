import socket
import time

EXTERNAL_HOST = '172.28.184.254'
CAROLINE_HOST = '152.3.54.6'

AMAZON_UPS_HOST = CAROLINE_HOST  # IP address of the UPS server
AMAZON_UPS_PORT = 54321 # UPS server port
ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ups_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

while True:
    try:
        ups_socket.connect((AMAZON_UPS_HOST, AMAZON_UPS_PORT))
        print("connected to UPS server")
        break
    except Exception as e:
        print("UPS server not ready yet")
        print("")
        time.sleep(2)
