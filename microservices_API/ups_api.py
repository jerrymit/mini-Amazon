# this is a server api that receives the message from UPS client
import socket
import threading
import time 
from ups_api_subfiles.transmit_msg import *


# Define a function to handle incoming connections and messages
def handle_connection(conn, addr):
    # Receive the incoming message from the connection
    umsg = receive_UMessage(conn)
    # Check the type of the incoming message and process it accordingly
    if umsg.HasField("truckAtWH"):
        print("Received UTruckAtWH message:", umsg.truckAtWH)
        # Process the UTruckAtWH message here
    elif umsg.HasField("packageDelivered"):
        print("Received UPackageDelivered message:", umsg.packageDelivered)
        # Process the UPackageDelivered message here
    conn.close()

# Amazon - UPS socket
amazon_ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 6666 # UPS Port 
amazon_ups_socket.bind((host, port))
amazon_ups_socket.listen(5)


def main():
    # Loop indefinitely to accept incoming connections
    while True:
        # Wait for a new connection
        conn, addr = amazon_ups_socket.accept()
        # Create a new thread to handle the incoming connection and message
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        # Start the new thread
        t.start()

