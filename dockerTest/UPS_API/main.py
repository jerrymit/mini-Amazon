# this is a server api that receives the message from UPS client
import socket
import threading
import time 
from transmit_msg import *
from upsAPI_query import *
import os

#AMAZON_HOST = os.environ.get('AMAZON_HOST', '0.0.0.0')


LOCAL_HOST1 = '152.3.53.130'
LOCAL_HOST = '0.0.0.0'
EXTERNAL_HOST = '172.28.216.179'

AMAZON_HOST = LOCAL_HOST
AMAZON_PORT = 6543 # Amazon to UPS

WORLD_SERVICE_HOST = LOCAL_HOST
WORLD_SERVICE_PORT = 9487 # Internal Port 

# Define a function to handle incoming connections and messages
def handle_connection(umsg):
    
    # Check the type of the incoming message and process it accordingly
    if umsg.HasField("truckAtWH"):
        print("Received UTruckAtWH message:\n")
        # Process the UTruckAtWH message here
        package_id = umsg.truckAtWH.package_id
        truck_id = umsg.truckAtWH.truck_id
        # package table update
        give_package_truckid(package_id, truck_id)
        # add a open load request to request table
        add_open_request(package_id, "load")
        
    elif umsg.HasField("packageDelivered"):
        print("Received UPackageDelivered message:\n")
        # Process the UPackageDelivered message here
        package_id = umsg.packageDelivered.package_id
        update_package_status(package_id, "delivered")


def sendWorldIdtoWorldService(worldid):
    internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            internal_socket.connect((WORLD_SERVICE_HOST, WORLD_SERVICE_PORT))
            print("Connected to World Service")
            break
        except:
            print("World Service not ready yet")
            time.sleep(1)
    internal_socket.send(worldid)


if __name__ == '__main__':
    # Amazon - UPS socket
    # Setting up server
    print("Setting up server")
    amazon_ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    amazon_ups_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    amazon_ups_socket.bind((AMAZON_HOST, AMAZON_PORT))
    print("hello")
    amazon_ups_socket.listen(5)
    print("Waiting")
    conn, addr = amazon_ups_socket.accept()
    initWorld = receive_UtoAzConnect(conn)
    print(initWorld.worldid)
    sendWorldIdtoWorldService(str(initWorld.worldid).encode())
    print("World ID sent to World Service", initWorld.worldid)

    # Loop indefinitely to accept incoming connections
    
    while True:
        # Receive the incoming message from the connection
        umsg = receive_UMessage(conn)
        print(umsg)
        # Create a new thread to handle the incoming connection and message
        t = threading.Thread(target=handle_connection, args=(umsg,))
        # Start the new thread
        t.start()