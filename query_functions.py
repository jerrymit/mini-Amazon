from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server_models import Product, Warehouse, Shipment, Order, Cart

# Create the SQLAlchemy engine and session
db_url = "postgresql://postgres:passw0rd@127.0.0.1:5432/amazon"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


def add_product(description, count):
    session = Session()
    new_product = Product(description=description, count=count)
    session.add(new_product)
    session.commit()
    session.close()


