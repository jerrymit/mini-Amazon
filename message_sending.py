import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import invocated_files.world_amazon_pb2 as world_amazon_pb2
import invocated_files.amazon_ups_pb2 as amazon_ups_pb2
import time 



def send_purchase_more(amazon_world_socket, warehouse_id, products):
    seqnum = 1

    while True:
        # Create ACommands message with APurchaseMore information
        commands = world_amazon_pb2.ACommands()
        purchase_more = commands.buy.add()
        purchase_more.whnum = warehouse_id
        purchase_more.seqnum = seqnum

        for product in products:
            item = purchase_more.things.add()
            item.id = product['id']  # Add id field
            item.description = product['description']
            item.count = product['count']

        # Print the commands message before serialization
        print("Commands message before serialization:")
        print(commands)

        # Send ACommands message to the world server
        encoded_msg = commands.SerializeToString()
        _EncodeVarint(amazon_world_socket.send, len(encoded_msg), None)
        amazon_world_socket.send(encoded_msg)

        # Receive AResponses message from the world server
        var_int_buff = []
        while True:
            buf = amazon_world_socket.recv(1)
            var_int_buff += buf
            msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
            if new_pos != 0:
                break

        whole_msg = amazon_world_socket.recv(msg_len)
        responses = world_amazon_pb2.AResponses()
        responses.ParseFromString(whole_msg)

        print("Responses message:")
        print(responses)

        # Check for ack in AResponses message
        if seqnum in responses.acks:
            break

        # Wait before sending the request again
        time.sleep(1)

        seqnum += 1

def request_truck_to_warehouse(amazon_ups_socket, warehouse_id, package_id, items, x, y, user_id):
    # Create an AMessage with ASendTruck information
    message = amazon_ups_pb2.AMessage()
    send_truck = message.sendTruck
    send_truck.package_id = package_id
    send_truck.warehouse_id = warehouse_id
    if user_id is not None:
        send_truck.user_id = user_id
    send_truck.x = x  # Set x coordinate of the destination
    send_truck.y = y  # Set y coordinate of the destination

    for item in items:
        product = send_truck.items.add()
        product.description = item['description']
        product.count = item['count']

    # Send AMessage to UPS
    print("AMessage to UPS message:")
    print(message)
    encoded_msg = message.SerializeToString()
    _EncodeVarint(amazon_ups_socket.send, len(encoded_msg), None)
    amazon_ups_socket.send(encoded_msg)
    
def receive_truck_at_wh(amazon_ups_socket):
    var_int_buff = []
    while True:
        buf = amazon_ups_socket.recv(1)
        if not buf:
            # If nothing is received, wait for a moment and try again
            time.sleep(1)
            continue
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_msg = amazon_ups_socket.recv(msg_len)

    received_msg = amazon_ups_pb2.UMessage()
    received_msg.ParseFromString(whole_msg)

    return received_msg
