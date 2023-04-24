# this is a server api that receives the message from UPS client
import socket
import threading
import time 
from ups_api_subfiles.transmit_msg import *
from ups_api_subfiles.database_funcs import *

LOCAL_HOST = '152.3.53.130'
EXTERNAL_HOST = '172.28.216.179'

AMAZON_HOST = LOCAL_HOST
AMAZON_PORT = 6543 # Amazon to UPS

WORLD_SERVICE_HOST = LOCAL_HOST
WORLD_SERVICE_PORT = 9487 # Internal Port 

# Define a function to handle incoming connections and messages
def handle_connection(conn, addr):
    # Receive the incoming message from the connection
    umsg = receive_UMessage(conn)
    # Check the type of the incoming message and process it accordingly
    if umsg.HasField("truckAtWH"):
        print("Received UTruckAtWH message:")
        # Process the UTruckAtWH message here
        package_id = umsg.truckAtWH.package_id
        truck_id = umsg.truckAtWH.truck_id
        # package table update
        give_package_truckid(package_id, truck_id)
        # add a open load request to request table
        add_open_request(package_id, "load")
        
    elif umsg.HasField("packageDelivered"):
        print("Received UPackageDelivered message:")
        # Process the UPackageDelivered message here
        package_id = umsg.packageDelivered.package_id
        update_package_status(package_id, "delivered")
    conn.close()


def sendWorldIdtoWorldService(worldid):
    internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    internal_socket.connect((WORLD_SERVICE_HOST, WORLD_SERVICE_PORT))
    internal_socket.send(worldid)


if __name__ == '__main__':
    # Amazon - UPS socket
    # Setting up server
    amazon_ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    amazon_ups_socket.bind((AMAZON_HOST, AMAZON_PORT))
    amazon_ups_socket.listen(5)
    print("Waiting")
    external_ups, addr = amazon_ups_socket.accept()
    initWorld = receive_UtoAzConnect(external_ups)
    print(initWorld.worldid)
    sendWorldIdtoWorldService(str(initWorld.worldid).encode())
    print("World ID sent to World Service")

    # Loop indefinitely to accept incoming connections
    
    while True:
        # Wait for a new connection
        conn, addr = amazon_ups_socket.accept()
        # Create a new thread to handle the incoming connection and message
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        # Start the new thread
        t.start()