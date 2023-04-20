import threading
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import invocated_files.internal_pb2 as internal_pb2
import invocated_files.amazon_ups_pb2 as amazon_ups_pb2


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
    
def construct_amessage_from_request(warehouse_id, package_id, request):
    message = amazon_ups_pb2.AMessage()
    send_truck = message.sendTruck
    send_truck.package_id = package_id
    send_truck.warehouse_id = warehouse_id
    if request.user_id is not None:
        send_truck.user_id = request.user_id
    send_truck.x = request.x  # Set x coordinate of the destination
    send_truck.y = request.y  # Set y coordinate of the destination
    for product in request.product:
        a_item = send_truck.items.add()
        a_item.description = product.description
        a_item.count = product.count
    return message 
