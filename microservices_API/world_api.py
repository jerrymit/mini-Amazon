# this is a client api that is used to communicate with the world server and the UPS server
import socket
import time
from world_api_subfiles.construct_msg import *
from microservices_API.world_api_subfiles.query_funcs import *
from world_api_subfiles.transmit_msg import *

# set the IP address and port number of the world server
WORLD_HOST = '127.0.0.1'  # replace with the actual IP address of the world server
WORLD_PORT = 23456

# set the IP address and port number of the UPS server
AMAZON_UPS_HOST = '172.28.216.179'  # IP address of the UPS server
AMAZON_UPS_PORT = 54321 # UPS server port



# To UPS Socket
ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        ups_socket.connect((AMAZON_UPS_HOST, AMAZON_UPS_PORT))
        break
    except:
        print("UPS server not ready yet")
        time.sleep(1)


# To World Socket
world_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
world_socket.connect((WORLD_HOST, WORLD_PORT))

# # Internal UI Socket
# internal_ui = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # set the IP address and port number of the world server
# ip = '127.0.0.1' 
# port = 7777
# internal_ui.connect((ip, port))



def getWorldId():
    # Internal UPS Socket
    internal_ups = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the IP address and port number of the world server
    INTERNAL_WORLD_SERVICE_HOST = '127.0.0.1' 
    INTERNAL_WORLD_SERVICE_PORT = 9487
    internal_ups.bind((INTERNAL_WORLD_SERVICE_HOST, INTERNAL_WORLD_SERVICE_PORT))
    internal_ups.listen(5)
    print("waiting for world id...")
    conn, addr = internal_ups.accept()
    worldid = int(conn.recv(1024).decode())
    print("world id received: ", worldid)
    return worldid

def initialize_world():
    worldid = getWorldId()
    # add 100 AInitWarehouse messages to the AConnect message
    ###### DB
    init_warehouse_list = []
    for i in range(10):
        for j in range(10):
            wh = construct_AInitWarehouse(i * 10 + j, i * 5, j * 5)
            init_warehouse_list.append(wh)

    connect_msg = construct_AConnect(worldid, init_warehouse_list, True)
    send_command(connect_msg, world_socket)
    world_connect_response = receive_AConnected(world_socket)
    if(world_connect_response.result == "connected!"):
        print("Connection to world server successful!")
        conneted_msg = construct_AzConnected(world_connect_response.worldid, "success")
        send_command(conneted_msg, ups_socket)
    else:
        print("Connection to world server failed.")
        conneted_msg = construct_AzConnected(world_connect_response.worldid, "failed")
        send_command(conneted_msg, ups_socket)
        raise ConnectionError("Failed to connect to world server")

def inform_ui():
    retry_count = 0
    max_retries = 10
    while not connected and retry_count < max_retries:
        time.sleep(2)
        try:
            ups_socket.connect((ip, port))
            print("Conneted to internal UI API")
            connected = True
        except:
            retry_count += 1
            print("Connection to internal UI failed. Retrying...")
    ups_socket.send("world is ready")

if __name__ == '__main__':
    initialize_world()
    # inform_ui()

    while True:
        # get open requests from the DB
        requests = getOpenRequest()
        buy = []
        topack = []
        load = [] 
        queries =[] 
        #simspeed = None 
        #disconnect = None 
        acks = None
        for request in requests:
            if(request.type == "purchase"):
                seqnum = request.request_id
                package_id = request.pk_id
                orders = getOrdersWithPackageid(package_id)
                whnum = 0
                products = []
                for order in orders:
                    product = getProductWithProductid(order.product_id)
                    product_id = product.product_id
                    description = product.description
                    count = order.quantity
                    Aproduct = construct_AProcuct(product_id, description, count)
                    products.append(Aproduct)
                    whnum = order.warehouse_id
                purchase_more = construct_APurchaseMore(whnum, products, seqnum)
                buy.append(purchase_more)
            elif(request.type == "pack"):
                seqnum = request.request_id
                package_id = request.pk_id
                orders = getOrdersWithPackageid(package_id)
                whnum = 0
                products = []
                for order in orders:
                    product = getProductWithProductid(order.product_id)
                    product_id = product.product_id
                    description = product.description
                    count = order.quantity
                    Aproduct = construct_AProcuct(product_id, description, count)
                    products.append(Aproduct)
                pack = construct_APack(whnum, products, package_id, seqnum)
                topack.append(pack)
            elif(request.type == "load"):
                seqnum = request.request_id
                package_id = request.pk_id
                truck_id = request.truck_id
                orders = getOrdersWithPackageid(package_id)
                whnum = 0
                for order in orders:
                    whnum = order.warehouse_id
                APutOnTruck = construct_APutOnTruck(truck_id, whnum, package_id, seqnum)
                load.append(APutOnTruck)

        # only construct and send ACommands if there exist buy, topack, load, queries, or acks
        if buy or topack or load or queries or acks:
            commands = construct_ACommands(buy, topack, load, queries, acks)
            print("sending commands to world server", commands)
            # send Acommand to world server
            send_command(commands, world_socket)
        
        # receive AResponse from world server
        AResponse = receive_AResponse(world_socket)
        if len(AResponse.acks) > 0:
            acksList = construct_acksList_from_response(AResponse)
            # update the database to ACK and send acks to UPS server
            ack_mechanics(acksList, world_socket)
            proceed_after_ACK(acksList, world_socket)
            
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
