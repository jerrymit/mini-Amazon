from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random, socket, json

db_url = "postgresql://postgres:amazon@127.0.0.1:5432/amazon"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

def frontend_connection():
    # create a TCP/IP socket
    internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()
    # set the port for UPS to connect to
    port = 55555
    internal_socket.bind((host, port))
    return internal_socket
    
def add_commodity():
    session = Session()

    # create commodities
    commodities = [
        ('apple', 20),
        ('book', 20),
        ('cat', 15),
        ('dog', 10),
        ('banana', 30),
        ('cloth', 30),
        ('shoes', 50),
        ('kimchi', 100),
        ('TV', 40),
        ('coach', 30),
        ('ball', 25),
        ('beef noodle', 10),
    ]

    for description, count in commodities:
        commodity = Commodity(description=description, count=count)
        session.add(commodity)

    session.commit()
    session.close()
    
def add_product():
    session = Session()

    # create commodities
    products = [
        ('apple'),
        ('book'),
        ('cat'),
        ('dog'),
        ('banana'),
        ('cloth'),
        ('shoes'),
        ('kimchi'),
        ('TV'),
        ('coach'),
        ('ball'),
        ('beef noodle'),
    ]

    for description in products:
        commodity = Product(description=description)
        session.add(commodity)

    session.commit()
    session.close()
    
def add_warehouse():
    session = Session()

    # create commodities
    warehouses = [
        (1, 1),
        (2, 2),
        (3, 3),
    ]

    for location_x, location_y in warehouses:
        warehouse = Warehouse(location_x=location_x, location_y=location_y)
        session.add(warehouse)

    session.commit()
    session.close()

def add_package(destination_x, destination_y, user_id):
    session = Session()
    new_package = Package(destination_x=destination_x, destination_y=destination_y, user_id = user_id)
    session.add(new_package)
    session.commit()
    new_package_id = new_package.package_id
    session.close()
    return new_package_id

def add_order(product_id, count, pk_id, warehouse_id):
    session = Session()

    # Retrieve the product, warehouse, and package objects based on the provided IDs
    product = session.query(Product).get(product_id)
    warehouse = session.query(Warehouse).get(warehouse_id)
    package = session.query(Package).get(pk_id)

    # Create a new order with the retrieved product, quantity, warehouse, and package objects
    new_order = Order(product=product, quantity=count, warehouse=warehouse, package=package)

    # Add the new order to the session and commit the transaction
    session.add(new_order)
    session.commit()
    session.close()

def add_request(pk_id):
    session = Session()
    package = session.query(Package).get(pk_id)
    new_request = Request(type = "purchase", status = "Open", package=package)
    session.add(new_request)
    session.commit()
    session.close()