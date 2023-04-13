import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import world_amazon_pb2
import amazon_ups_pb2
import time 


def amazon_ups_server():
    # create a socket object
    amazon_ups_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    # set the port for UPS to connect to
    port = 34567
    print("hostname", host)

    # bind the socket to a specific address and port
    amazon_ups_socket.bind((host, port))

    # listen for incoming connections
    amazon_ups_socket.listen(5)

    # wait for a connection
    print('Waiting for a connection...')
    client_socket, addr = amazon_ups_socket.accept()

    # print the client address
    print(f'Got a connection from {addr}')
    return client_socket

def worldid_from_ups(amazon_ups_socket):
    # receive a message from the UPS client
    var_int_buff = []
    while True:
        buf = amazon_ups_socket.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_msg = amazon_ups_socket.recv(msg_len)

    # parse the received message as an AConnected message
    UToA_msg = amazon_ups_pb2.UtoAzConnect()
    UToA_msg.ParseFromString(whole_msg)

    # print the received message
    print("Received message with worldid:", UToA_msg.worldid)
    return UToA_msg.worldid

def amazon_world_client(amazon_ups_socket, worldid):
    # create a socket object
    amazon_world_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set the IP address and port number of the world server
    ip = '127.0.0.1'  # replace with the actual IP address of the world server
    port = 23456

    # connect to the world server
    AToU_msg = amazon_ups_pb2.AzConnected()
    AToU_msg.worldid = worldid
    connected = False
    retry_count = 0
    max_retries = 10
    while not connected and retry_count < max_retries:
        time.sleep(2)
        try:
            amazon_world_socket.connect((ip, port))
            connected = True
        except:
            retry_count += 1
            print("Connection to world server failed. Retrying...")

    if not connected:
        AToU_msg.result = "fail"
        encoded_msg = AToU_msg.SerializeToString()
        _EncodeVarint(amazon_ups_socket.send, len(encoded_msg), None)
        amazon_ups_socket.send(encoded_msg)
        raise Exception("Unable to connect to world server.")
    

    # create an AConnect message to send to the world server
    connect_msg = world_amazon_pb2.AConnect()
    connect_msg.isAmazon = True  # set the isAmazon field to True
    connect_msg.worldid = worldid  # set the worldid field to the received worldid

    # add 100 AInitWarehouse messages to the AConnect message
    for i in range(10):
        for j in range(10):
            init_warehouse = connect_msg.initwh.add()
            init_warehouse.id = i * 10 + j
            init_warehouse.x = i * 5
            init_warehouse.y = j * 5

    # encode the AConnect message and send it to the world server
    encoded_msg = connect_msg.SerializeToString()
    _EncodeVarint(amazon_world_socket.send, len(encoded_msg), None)
    amazon_world_socket.send(encoded_msg)

    # receive a message from the world server
    var_int_buff = []
    while True:
        buf = amazon_world_socket.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_msg = amazon_world_socket.recv(msg_len)

    # parse the received message as an AConnected message
    connected_msg = world_amazon_pb2.AConnected()
    connected_msg.ParseFromString(whole_msg)

    # print the received message
    print("connected_msg.result: ", connected_msg.result)
    if (connected_msg.result == "connected!"):
        print("Connection to world server successful!")
        # send a message to the UPS client
        AToU_msg.result = "success"
        # encode the AConnect message and send it to the world server

        encoded_msg = AToU_msg.SerializeToString()
        _EncodeVarint(amazon_ups_socket.send, len(encoded_msg), None)
        amazon_ups_socket.send(encoded_msg)
        print("Sent message to UPS with worldid:", AToU_msg.worldid)

    return amazon_world_socket

if __name__ == "__main__":
    amazon_ups_socket = amazon_ups_server()
    while True:
        try:
            worldid = worldid_from_ups(amazon_ups_socket)
            amazon_world_socket = amazon_world_client(amazon_ups_socket, worldid)
            break
        except:
            continue
