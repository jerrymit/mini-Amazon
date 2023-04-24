from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tables import *
import random, socket, json

db_url = "postgresql://postgres:passw0rd@127.0.0.1:5432/amazon2"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

def getOrdersWithPackageid(package_id):
    print("getOrdersWithPackageid\n")
    session = Session()

    # query all orders with package_id = 1
    orders = session.query(Order).filter(Order.package_id == package_id).all()

    # print the description of the products in the orders
    for order in orders:
        print("product id: ", order.product.product_id)
        print("quantity: ", order.quantity)
        print("warehouse_id: ", order.warehouse_id)
        print("package_id: ", order.package_id)
        
    print("====================================")
    session.close()
    return orders

def getOpenRequest():
    session = Session()
    open_requests = session.query(Request).filter_by(status='Open').all()
    # Print the results
    for request in open_requests:
        print(request.request_id, request.type, request.status, request.package.package_id)
    session.close()

    return open_requests

def getProductWithProductid(product_id):
    print("get_Product\n")
    session = Session()
    product = session.query(Product).filter_by(product_id=product_id).first()
    print("Product id: ", product.product_id)
    print("Description: ", product.description)
    print("====================================")
    session.close()
    return product

def get_Package(package_id):
    print("get_Package\n")
    session = Session()
    package = session.query(Package).filter_by(package_id=package_id).first()
    print("Package id: ", package.package_id)
    print("Destination x: ", package.destination_x)
    print("Destination y: ", package.destination_y)
    print("User id: ", package.user_id)
    print("====================================")
   
    session.close()
    return package

def update_request_status_to_ack(request_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Request).filter_by(request_id=request_id).first()
    request.status = 'ACK'
    session.commit()
    session.close()

def update_request_status_to_open(request_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Request).filter_by(request_id=request_id).first()
    request.status = 'open'
    session.commit()
    session.close()

def get_request_with_ack(request_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    request = session.query(Request).filter_by(request_id=request_id).first()
    session.close()
    print("request_id: ", request.request_id)
    print("type: ", request.type)
    return request

def add_open_request(package_id, type):
    session = Session()
    new_request = Request(type=type, status="open", pk_id=package_id)
    session.add(new_request)
    session.commit()
    session.close()

def delete_request(request_id):
    session = Session()
    request = session.query(Request).filter_by(request_id=request_id).first()
    session.delete(request)
    session.commit()
    session.close()

def update_package_status(package_id, status):
    session = Session()
    package = session.query(Package).filter_by(package_id=package_id).first()
    package.status = status
    session.commit()
    session.close()


if __name__ == "__main__":
    # update_request_status_to_ack(1)
    # add_pack_request(1)
    # delete_request(6)
    # update_request_status_to_open(1)
    pass

