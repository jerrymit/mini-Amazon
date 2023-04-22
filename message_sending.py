from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import invocated_files.world_amazon_pb2 as world_amazon_pb2
import invocated_files.amazon_ups_pb2 as amazon_ups_pb2
from utility import *
import time 





def send_purchase_more(amazon_world_socket, warehouse_id, frontend_request):
    seqnum = 1

    while True:
        commands = construct_purchase_to_world(warehouse_id, seqnum, frontend_request)

        # Print the commands message before serialization
        print("Purchase more message:")
        print(commands)

        # Send ACommands message to the world server
        encoded_msg = commands.SerializeToString()
        _EncodeVarint(amazon_world_socket.send, len(encoded_msg), None)
        amazon_world_socket.send(encoded_msg)

        # Receive AResponses message from the world server
        whole_msg = receive_response(amazon_world_socket)
        responses = world_amazon_pb2.AResponses()
        responses.ParseFromString(whole_msg)

        print("Purchase Responses message:")
        print(responses)

        # Check for ack in AResponses message
        if seqnum in responses.acks:
            if len(responses.arrived) > 0:
                ACK(amazon_world_socket, responses, "arrived")
                break 
            # Continue receive AResponses message from the world server
            while True:
                whole_msg = receive_response(amazon_world_socket)
                responses = world_amazon_pb2.AResponses()
                responses.ParseFromString(whole_msg)
                print("response: ", responses)
                if len(responses.arrived) > 0:
                    ACK(amazon_world_socket, responses, "arrived")
                    break 
            break

        # Wait before sending the request again
        time.sleep(1)

        seqnum += 1

def send_APack_to_world(amazon_world_socket, warehouse_id, shipid, frontend_request):
    seqnum = 1
    while True:
        commands = construct_APack_to_world(warehouse_id, frontend_request, shipid, seqnum)

        # Print the commands message before serialization
        print("APack message:")
        print(commands)

        # Send ACommands message to the world server
        encoded_msg = commands.SerializeToString()
        _EncodeVarint(amazon_world_socket.send, len(encoded_msg), None)
        amazon_world_socket.send(encoded_msg)

        # Receive AResponses message from the world server
        whole_msg = receive_response(amazon_world_socket)
        responses = world_amazon_pb2.AResponses()
        responses.ParseFromString(whole_msg)
        print("APacked Responses message:")
        print(responses)
        # Check for ack in AResponses message
        if seqnum in responses.acks:
            if len(responses.ready) > 0:
                ACK(amazon_world_socket, responses, "ready")
                break 
            # Continue receive AResponses message from the world server
            while True:
                whole_msg = receive_response(amazon_world_socket)
                responses = world_amazon_pb2.AResponses()
                responses.ParseFromString(whole_msg)
                print("response: ", responses)
                if len(responses.ready) > 0:
                    ACK(amazon_world_socket, responses, "ready")
                    break 
            break
        # Wait before sending the request again
        time.sleep(1)
        seqnum += 1

def request_truck_to_warehouse_bu(amazon_ups_socket, warehouse_id, package_id, items, x, y, user_id):
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

def request_truck_to_warehouse(amazon_ups_socket, warehouse_id, package_id, request):
    # Create an AMessage with ASendTruck information
    message = construct_ASendTruck_from_request(warehouse_id, package_id, request)

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
