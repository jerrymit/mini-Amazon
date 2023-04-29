# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: world_ups.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fworld_ups.proto\".\n\nUInitTruck\x12\n\n\x02id\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\"J\n\x08UConnect\x12\x0f\n\x07worldid\x18\x01 \x01(\x03\x12\x1b\n\x06trucks\x18\x02 \x03(\x0b\x32\x0b.UInitTruck\x12\x10\n\x08isAmazon\x18\x03 \x02(\x08\"-\n\nUConnected\x12\x0f\n\x07worldid\x18\x01 \x02(\x03\x12\x0e\n\x06result\x18\x02 \x02(\t\":\n\tUGoPickup\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12\x0c\n\x04whid\x18\x02 \x02(\x05\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\"R\n\tUFinished\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\x12\x0e\n\x06status\x18\x04 \x02(\t\x12\x0e\n\x06seqnum\x18\x05 \x02(\x03\"C\n\rUDeliveryMade\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12\x11\n\tpackageid\x18\x02 \x02(\x03\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\"<\n\x11UDeliveryLocation\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\"S\n\nUGoDeliver\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12$\n\x08packages\x18\x02 \x03(\x0b\x32\x12.UDeliveryLocation\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\"9\n\x04UErr\x12\x0b\n\x03\x65rr\x18\x01 \x02(\t\x12\x14\n\x0coriginseqnum\x18\x02 \x02(\x03\x12\x0e\n\x06seqnum\x18\x03 \x02(\x03\")\n\x06UQuery\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12\x0e\n\x06seqnum\x18\x02 \x02(\x03\"O\n\x06UTruck\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12\x0e\n\x06status\x18\x02 \x02(\t\x12\t\n\x01x\x18\x03 \x02(\x05\x12\t\n\x01y\x18\x04 \x02(\x05\x12\x0e\n\x06seqnum\x18\x05 \x02(\x03\"\x97\x01\n\tUCommands\x12\x1b\n\x07pickups\x18\x01 \x03(\x0b\x32\n.UGoPickup\x12\x1f\n\ndeliveries\x18\x02 \x03(\x0b\x32\x0b.UGoDeliver\x12\x10\n\x08simspeed\x18\x03 \x01(\r\x12\x12\n\ndisconnect\x18\x04 \x01(\x08\x12\x18\n\x07queries\x18\x05 \x03(\x0b\x32\x07.UQuery\x12\x0c\n\x04\x61\x63ks\x18\x06 \x03(\x03\"\xa4\x01\n\nUResponses\x12\x1f\n\x0b\x63ompletions\x18\x01 \x03(\x0b\x32\n.UFinished\x12!\n\tdelivered\x18\x02 \x03(\x0b\x32\x0e.UDeliveryMade\x12\x10\n\x08\x66inished\x18\x03 \x01(\x08\x12\x0c\n\x04\x61\x63ks\x18\x04 \x03(\x03\x12\x1c\n\x0btruckstatus\x18\x05 \x03(\x0b\x32\x07.UTruck\x12\x14\n\x05\x65rror\x18\x06 \x03(\x0b\x32\x05.UErr')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'world_ups_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _UINITTRUCK._serialized_start=19
  _UINITTRUCK._serialized_end=65
  _UCONNECT._serialized_start=67
  _UCONNECT._serialized_end=141
  _UCONNECTED._serialized_start=143
  _UCONNECTED._serialized_end=188
  _UGOPICKUP._serialized_start=190
  _UGOPICKUP._serialized_end=248
  _UFINISHED._serialized_start=250
  _UFINISHED._serialized_end=332
  _UDELIVERYMADE._serialized_start=334
  _UDELIVERYMADE._serialized_end=401
  _UDELIVERYLOCATION._serialized_start=403
  _UDELIVERYLOCATION._serialized_end=463
  _UGODELIVER._serialized_start=465
  _UGODELIVER._serialized_end=548
  _UERR._serialized_start=550
  _UERR._serialized_end=607
  _UQUERY._serialized_start=609
  _UQUERY._serialized_end=650
  _UTRUCK._serialized_start=652
  _UTRUCK._serialized_end=731
  _UCOMMANDS._serialized_start=734
  _UCOMMANDS._serialized_end=885
  _URESPONSES._serialized_start=888
  _URESPONSES._serialized_end=1052
# @@protoc_insertion_point(module_scope)
