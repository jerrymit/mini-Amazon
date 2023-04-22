# this is a client api that is used to communicate with the world server and the UPS server
import socket
import time
from world_api_subfiles.construct_msg import *
from world_api_subfiles.query_functions import *
from world_api_subfiles.transmit_msg import *


# To UPS Socket
amazon_ups_as_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set the IP address and port number of the UPS server
ip = '127.0.0.1'  # IP address of the UPS server
port = 6677 # UPS server port
amazon_ups_as_client.connect((ip, port))

# To World Socket
amazon_world_as_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set the IP address and port number of the world server
ip = '127.0.0.1'  # replace with the actual IP address of the world server
port = 23456
amazon_world_as_client.connect((ip, port))

# Internal UI Socket
internal_ui = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set the IP address and port number of the world server
ip = '127.0.0.1' 
port = 7777
internal_ui.connect((ip, port))

def initialize_world():
    retry_count = 0
    max_retries = 10
    while not connected and retry_count < max_retries:
        time.sleep(2)
        try:
            amazon_ups_as_client.connect((ip, port))
            print("Conneted to UPS server")
            connected = True
        except:
            retry_count += 1
            print("Connection to UPS server failed. Retrying...")
    UtoAzConnect = receive_UtoAzConnect(amazon_ups_as_client)
    worldid = UtoAzConnect.worldid
    while not connected and retry_count < max_retries:
        time.sleep(2)
        try:
            amazon_world_as_client.connect((ip, port))
            print("Initial connect to world server")
            connected = True
        except:
            retry_count += 1
            print("Connection to world server failed. Retrying...")

    # add 100 AInitWarehouse messages to the AConnect message
    init_warehouse_list = []
for i in range(10):
    for j in range(10):
        wh = construct_AInitWarehouse(i * 10 + j, i * 5, j * 5)
        init_warehouse_list.append(wh)
    
    pass


while True:
    # create ACommand
    commands = world_amazon_pb2.ACommands()
        # need database query here to contine

    # send Acommand to world server
    send_command(commands, amazon_world_as_client)
    # receive AResponse from world server
    AResponse = receive_response(amazon_world_as_client)
    # ACK to world server
    ACommands_ACK = construct_ACK(AResponse)
    send_command(ACommands_ACK, amazon_world_as_client)
    
    # DB query
    # for each ACK, get the query result which has the same seqnum as ACK
        # change the status from OPEN to ACK
        # if type == APurchaseMore
            # Add a Pack rquest with OPEN status and package_id from the query result
        # if type == PACK 
            # with package_id, get user_id (optional), warehouse_id, x, y from query
            # with package id, get all the products from query 
                # create AItem for each description and count of the product
            # create AsendTruck with package_id, warehouse_id, user_id, x, y, and AItem
            # create and send AMessage with ASendTruck type to UPS server
        # if type == LOAD 
            # with package_id, get truck_id and warehouse_id
            # Create and send AMessage with ATruckLoaded type to UPS server
    pass
