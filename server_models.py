from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'amazon_product'
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    count = Column(Integer)

class Warehouse(Base):
    __tablename__ = 'amazon_warehouse'
    warehouse_id = Column(Integer, primary_key=True)
    location_x = Column(Integer)
    location_y = Column(Integer)

class Shipment(Base):
    __tablename__ = 'amazon_shipment'
    shipment_id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey('amazon_warehouse.warehouse_id'))
    destination_x = Column(Integer)
    destination_y = Column(Integer)
    status = Column(String(200), default="ordering")
    create_time = Column(DateTime)
    truck_id = Column(Integer)

    warehouse = relationship("Warehouse", backref="shipments")

class Order(Base):
    __tablename__ = 'amazon_order'
    order_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('amazon_product.id'))
    quantity = Column(Integer)
    order_time = Column(DateTime)
    shipment_id = Column(Integer, ForeignKey('amazon_shipment.shipment_id'))

    product = relationship("Product")
    shipment = relationship("Shipment", backref="orders")

class Cart(Base):
    __tablename__ = 'amazon_cart'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('amazon_product.id'))
    quantity = Column(Integer, default=1)

    product = relationship("Product")
