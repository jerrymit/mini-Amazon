from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import invocated_files.amazon_ups_pb2 as amazon_ups_pb2
import invocated_files.world_amazon_pb2 as world_amazon_pb2


# Amazon to world server
def construct_AInitWarehouse(id, x, y):
    init_warehouse = world_amazon_pb2.AInitWarehouse()
    init_warehouse.id = id
    init_warehouse.x = x
    init_warehouse.y = y
    return init_warehouse

def construct_AConnect(worldid, initwh, isAmazon):
    connect = world_amazon_pb2.AConnect()
    connect.worldid = worldid
    connect.initwh.extend(initwh)
    connect.isAmazon = isAmazon
    return connect

def construct_AProcuct(id, description, count):
    product = world_amazon_pb2.AProduct()
    product.id = id
    product.description = description
    product.count = count
    return product

def construct_APurchaseMore(whnum, things, seqnum):
    purchase_more = world_amazon_pb2.APurchaseMore()
    purchase_more.whnum = whnum
    purchase_more.things.extend(things)
    purchase_more.seqnum = seqnum
    return purchase_more

def construct_APack(whnum, things, packageid, seqnum):
    pack = world_amazon_pb2.APack()
    pack.whnum = whnum
    pack.things.extend(things)
    pack.shipid = packageid
    pack.seqnum = seqnum
    return pack
    
def construct_APutOnTruck(whnum, things, packageid, seqnum):
    put_on_truck = world_amazon_pb2.APutOnTruck()
    put_on_truck.whnum = whnum
    put_on_truck.things.extend(things)
    put_on_truck.shipid = packageid
    put_on_truck.seqnum = seqnum
    return put_on_truck

def construct_AQuery(packageid, seqnum):
    query = world_amazon_pb2.AQuery()
    query.packageid = packageid
    query.seqnum = seqnum
    return query

def construct_ACommands(buy, topack, load, queries, simspeed, disconnect, acks):
    commands = world_amazon_pb2.ACommands()
    commands.buy.extend(buy)
    commands.topack.extend(topack)
    commands.load.extend(load)
    commands.queries.extend(queries)
    commands.simspeed = simspeed
    commands.disconnect = disconnect
    commands.acks.extend(acks)
    return commands
    
def construct_ACK(AResponse):
    # Extract the seqnum values from the APacked and ALoaded messages
    seqnums = []
    for arrived_msg in AResponse.arrived:
        seqnums.append(arrived_msg.seqnum)
    for packed_msg in AResponse.ready:
        seqnums.append(packed_msg.seqnum)
    for loaded_msg in AResponse.loaded:
        seqnums.append(loaded_msg.seqnum)
    for error_msg in AResponse.error:
        seqnums.append(error_msg.seqnum)
    for status_msg in AResponse.packagestatus:
        seqnums.append(status_msg.seqnum)

    ACommands_ACK = world_amazon_pb2.ACommands()
    ACommands_ACK.acks.extend(seqnums)
    return ACommands_ACK

# Amazon to UPS client
def construct_AzConnected(worldid, result):
    Az_connected = amazon_ups_pb2.AzConnected()
    Az_connected.worldid = worldid
    Az_connected.result = result
    return Az_connected

def construct_AItem(description, count):
    item = amazon_ups_pb2.AItem()
    item.description = description
    item.count = count
    return item

def construct_ASendTruck(package_id, warehouse_id, user_id, x, y, items):
    send_truck = amazon_ups_pb2.ASendTruck()
    send_truck.package_id = package_id
    send_truck.warehouse_id = warehouse_id
    send_truck.user_id = user_id
    send_truck.x = x
    send_truck.y = y
    send_truck.items.extend(items)
    return send_truck

def construct_ATruckLoaded(truck_id, warehouse_id, package_id):
    truck_loaded = amazon_ups_pb2.ATruckLoaded()
    truck_loaded.truck_id = truck_id
    truck_loaded.warehouse_id = warehouse_id
    truck_loaded.package_id = package_id
    return truck_loaded