import threading
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import invocated_files.internal_pb2 as internal_pb2
import invocated_files.amazon_ups_pb2 as amazon_ups_pb2
import invocated_files.world_amazon_pb2 as world_amazon_pb2
import json


# Define a global variable to store the current package ID
current_package_id = 0

# Define a lock to protect access to the current package ID variable
id_lock = threading.Lock()

# Define a function to generate a new package ID
def generate_package_id():
    global current_package_id
    with id_lock:
        current_package_id += 1
        return current_package_id
        
def ACK(socket, responses, type):
    ack = world_amazon_pb2.ACommands()
    if type == "arrived":
        for arrived in responses.arrived:
            ack.acks.append(arrived.seqnum)
    elif type == "ready":
        for ready in responses.ready:
            ack.acks.append(ready.seqnum)

    print("purchase ACK:")
    print(ack)
    # Send ACommands message to the world server
    encoded_msg = ack.SerializeToString()
    _EncodeVarint(socket.send, len(encoded_msg), None)
    socket.send(encoded_msg)

def receive_response(socket):
    # Receive AResponses message from the world server
    var_int_buff = []
    while True:
        buf = socket.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break

    whole_msg = socket.recv(msg_len)
    return whole_msg


def construct_purchase_to_world(warehouse_id, seqnum, frontend_request):
    message = world_amazon_pb2.ACommands()
    purchase_more = message.buy.add()
    purchase_more.whnum = warehouse_id
    purchase_more.seqnum = seqnum

    products_info = [(d['product_id'], d['description'], d['quantity']) for d in frontend_request if 'product_id' in d and 'description' in d and 'quantity' in d]
    for product_id, description, quantity in products_info:
            item = world_amazon_pb2.AProduct()
            item.id = product_id # Need to change this
            item.description = description
            item.count = quantity
            purchase_more.things.append(item)
    return message

def construct_APack_to_world(warehouse_id, frontend_request, shipid, seqnum):
    message = world_amazon_pb2.ACommands()
    pack = message.topack.add()
    pack.whnum = warehouse_id
    pack.shipid = shipid
    pack.seqnum = seqnum

    products_info = [(d['product_id'], d['description'], d['quantity']) for d in frontend_request if 'product_id' in d and 'description' in d and 'quantity' in d]
    for product_id, description, quantity in products_info:
            item = world_amazon_pb2.AProduct()
            item.id = product_id # Need to change this
            item.description = description
            item.count = quantity
            pack.things.append(item)
    return message
     
def construct_ASendTruck_from_request(warehouse_id, package_id, frontend_request):
    message = amazon_ups_pb2.AMessage()
    send_truck = message.sendTruck
    send_truck.package_id = package_id
    send_truck.warehouse_id = warehouse_id
    # if request.user_id is not None:
    #     send_truck.user_id = request.user_id
    # send_truck.x = request.x  # Set x coordinate of the destination
    # send_truck.y = request.y  # Set y coordinate of the destination
    # for product in request.product:
    #     a_item = send_truck.items.add()
    #     a_item.description = product.description
    #     a_item.count = product.count


    # process the incoming data
    print("in construct_ASendTruck_from_request")
    print("frontend_request: ", frontend_request)
    
    # Get destination_x and destination_y
    send_truck.x = int(frontend_request[0]['destination_x'])
    send_truck.y = int(frontend_request[1]['destination_y'])

    # Get description and quantity pairs
    product_info = [(d['description'], d['quantity']) for d in frontend_request if 'description' in d and 'quantity' in d]
    for description, quantity in product_info:
        a_item = amazon_ups_pb2.AItem()
        a_item.description = description
        a_item.count = int(quantity)
        send_truck.items.append(a_item)
        print(f"Product: {description}, Quantity: {quantity}")
    return message 
