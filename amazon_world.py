import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import world_amazon_pb2

# create a socket object
amazon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set the IP address and port number of the world server
ip = '127.0.0.1'  # replace with the actual IP address of the world server
port = 23456

# connect to the world server
amazon_socket.connect((ip, port))

# create an AConnect message to send to the world server
connect_msg = world_amazon_pb2.AConnect()
connect_msg.isAmazon = True  # set the isAmazon field to True

# encode the AConnect message and send it to the world server
encoded_msg = connect_msg.SerializeToString()
_EncodeVarint(amazon_socket.send, len(encoded_msg), None)
amazon_socket.send(encoded_msg)

# receive a message from the world server
var_int_buff = []
while True:
    buf = amazon_socket.recv(1)
    var_int_buff += buf
    msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
    if new_pos != 0:
        break
whole_msg = amazon_socket.recv(msg_len)

# parse the received message as an AConnected message
connected_msg = world_amazon_pb2.AConnected()
connected_msg.ParseFromString(whole_msg)

# print the received message
print(connected_msg)