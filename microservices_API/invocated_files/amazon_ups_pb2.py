# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: amazon_ups.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x61mazon_ups.proto\"\x1f\n\x0cUtoAzConnect\x12\x0f\n\x07worldid\x18\x01 \x02(\x03\".\n\x0b\x41zConnected\x12\x0f\n\x07worldid\x18\x01 \x02(\x03\x12\x0e\n\x06result\x18\x02 \x02(\t\"+\n\x05\x41Item\x12\x13\n\x0b\x64\x65scription\x18\x01 \x02(\t\x12\r\n\x05\x63ount\x18\x02 \x02(\x03\"t\n\nASendTruck\x12\x12\n\npackage_id\x18\x01 \x02(\x03\x12\x14\n\x0cwarehouse_id\x18\x02 \x02(\x03\x12\x0f\n\x07user_id\x18\x03 \x01(\x03\x12\t\n\x01x\x18\x04 \x02(\x03\x12\t\n\x01y\x18\x05 \x02(\x03\x12\x15\n\x05items\x18\x06 \x03(\x0b\x32\x06.AItem\"H\n\nUTruckAtWH\x12\x10\n\x08truck_id\x18\x01 \x02(\x03\x12\x14\n\x0cwarehouse_id\x18\x02 \x02(\x03\x12\x12\n\npackage_id\x18\x03 \x02(\x03\"J\n\x0c\x41TruckLoaded\x12\x10\n\x08truck_id\x18\x01 \x02(\x03\x12\x14\n\x0cwarehouse_id\x18\x02 \x02(\x03\x12\x12\n\npackage_id\x18\x03 \x02(\x03\"\'\n\x11UPackageDelivered\x12\x12\n\npackage_id\x18\x03 \x02(\x03\"X\n\x08UMessage\x12\x1e\n\ttruckAtWH\x18\x01 \x01(\x0b\x32\x0b.UTruckAtWH\x12,\n\x10packageDelivered\x18\x02 \x01(\x0b\x32\x12.UPackageDelivered\"N\n\x08\x41Message\x12\x1e\n\tsendTruck\x18\x01 \x01(\x0b\x32\x0b.ASendTruck\x12\"\n\x0btruckLoaded\x18\x02 \x01(\x0b\x32\r.ATruckLoaded')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'amazon_ups_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _UTOAZCONNECT._serialized_start=20
  _UTOAZCONNECT._serialized_end=51
  _AZCONNECTED._serialized_start=53
  _AZCONNECTED._serialized_end=99
  _AITEM._serialized_start=101
  _AITEM._serialized_end=144
  _ASENDTRUCK._serialized_start=146
  _ASENDTRUCK._serialized_end=262
  _UTRUCKATWH._serialized_start=264
  _UTRUCKATWH._serialized_end=336
  _ATRUCKLOADED._serialized_start=338
  _ATRUCKLOADED._serialized_end=412
  _UPACKAGEDELIVERED._serialized_start=414
  _UPACKAGEDELIVERED._serialized_end=453
  _UMESSAGE._serialized_start=455
  _UMESSAGE._serialized_end=543
  _AMESSAGE._serialized_start=545
  _AMESSAGE._serialized_end=623
# @@protoc_insertion_point(module_scope)
