# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobufs/node_messages.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobufs/node_messages.proto',
  package='chord',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1dprotobufs/node_messages.proto\x12\x05\x63hord\"\x1d\n\rInsertRequest\x12\x0c\n\x04song\x18\x01 \x02(\t\"\"\n\x0eInsertResponse\x12\x10\n\x08response\x18\x01 \x02(\t\"\x1d\n\rDeleteRequest\x12\x0c\n\x04song\x18\x01 \x02(\t\"\"\n\x0e\x44\x65leteResponse\x12\x10\n\x08response\x18\x01 \x02(\t\"\"\n\x14\x46indSuccessorRequest\x12\n\n\x02id\x18\x01 \x02(\r\"#\n\x15\x46indSuccessorResponse\x12\n\n\x02id\x18\x01 \x02(\r2\xce\x01\n\x0c\x43hordService\x12\x37\n\x06Insert\x12\x14.chord.InsertRequest\x1a\x15.chord.InsertResponse\"\x00\x12\x37\n\x06\x44\x65lete\x12\x14.chord.DeleteRequest\x1a\x15.chord.DeleteResponse\"\x00\x12L\n\rFindSuccessor\x12\x1b.chord.FindSuccessorRequest\x1a\x1c.chord.FindSuccessorResponse\"\x00'
)




_INSERTREQUEST = _descriptor.Descriptor(
  name='InsertRequest',
  full_name='chord.InsertRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='song', full_name='chord.InsertRequest.song', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=40,
  serialized_end=69,
)


_INSERTRESPONSE = _descriptor.Descriptor(
  name='InsertResponse',
  full_name='chord.InsertResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='chord.InsertResponse.response', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=71,
  serialized_end=105,
)


_DELETEREQUEST = _descriptor.Descriptor(
  name='DeleteRequest',
  full_name='chord.DeleteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='song', full_name='chord.DeleteRequest.song', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=136,
)


_DELETERESPONSE = _descriptor.Descriptor(
  name='DeleteResponse',
  full_name='chord.DeleteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='chord.DeleteResponse.response', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=172,
)


_FINDSUCCESSORREQUEST = _descriptor.Descriptor(
  name='FindSuccessorRequest',
  full_name='chord.FindSuccessorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='chord.FindSuccessorRequest.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=174,
  serialized_end=208,
)


_FINDSUCCESSORRESPONSE = _descriptor.Descriptor(
  name='FindSuccessorResponse',
  full_name='chord.FindSuccessorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='chord.FindSuccessorResponse.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=210,
  serialized_end=245,
)

DESCRIPTOR.message_types_by_name['InsertRequest'] = _INSERTREQUEST
DESCRIPTOR.message_types_by_name['InsertResponse'] = _INSERTRESPONSE
DESCRIPTOR.message_types_by_name['DeleteRequest'] = _DELETEREQUEST
DESCRIPTOR.message_types_by_name['DeleteResponse'] = _DELETERESPONSE
DESCRIPTOR.message_types_by_name['FindSuccessorRequest'] = _FINDSUCCESSORREQUEST
DESCRIPTOR.message_types_by_name['FindSuccessorResponse'] = _FINDSUCCESSORRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

InsertRequest = _reflection.GeneratedProtocolMessageType('InsertRequest', (_message.Message,), {
  'DESCRIPTOR' : _INSERTREQUEST,
  '__module__' : 'protobufs.node_messages_pb2'
  # @@protoc_insertion_point(class_scope:chord.InsertRequest)
  })
_sym_db.RegisterMessage(InsertRequest)

InsertResponse = _reflection.GeneratedProtocolMessageType('InsertResponse', (_message.Message,), {
  'DESCRIPTOR' : _INSERTRESPONSE,
  '__module__' : 'protobufs.node_messages_pb2'
  # @@protoc_insertion_point(class_scope:chord.InsertResponse)
  })
_sym_db.RegisterMessage(InsertResponse)

DeleteRequest = _reflection.GeneratedProtocolMessageType('DeleteRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEREQUEST,
  '__module__' : 'protobufs.node_messages_pb2'
  # @@protoc_insertion_point(class_scope:chord.DeleteRequest)
  })
_sym_db.RegisterMessage(DeleteRequest)

DeleteResponse = _reflection.GeneratedProtocolMessageType('DeleteResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETERESPONSE,
  '__module__' : 'protobufs.node_messages_pb2'
  # @@protoc_insertion_point(class_scope:chord.DeleteResponse)
  })
_sym_db.RegisterMessage(DeleteResponse)

FindSuccessorRequest = _reflection.GeneratedProtocolMessageType('FindSuccessorRequest', (_message.Message,), {
  'DESCRIPTOR' : _FINDSUCCESSORREQUEST,
  '__module__' : 'protobufs.node_messages_pb2'
  # @@protoc_insertion_point(class_scope:chord.FindSuccessorRequest)
  })
_sym_db.RegisterMessage(FindSuccessorRequest)

FindSuccessorResponse = _reflection.GeneratedProtocolMessageType('FindSuccessorResponse', (_message.Message,), {
  'DESCRIPTOR' : _FINDSUCCESSORRESPONSE,
  '__module__' : 'protobufs.node_messages_pb2'
  # @@protoc_insertion_point(class_scope:chord.FindSuccessorResponse)
  })
_sym_db.RegisterMessage(FindSuccessorResponse)



_CHORDSERVICE = _descriptor.ServiceDescriptor(
  name='ChordService',
  full_name='chord.ChordService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=248,
  serialized_end=454,
  methods=[
  _descriptor.MethodDescriptor(
    name='Insert',
    full_name='chord.ChordService.Insert',
    index=0,
    containing_service=None,
    input_type=_INSERTREQUEST,
    output_type=_INSERTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Delete',
    full_name='chord.ChordService.Delete',
    index=1,
    containing_service=None,
    input_type=_DELETEREQUEST,
    output_type=_DELETERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FindSuccessor',
    full_name='chord.ChordService.FindSuccessor',
    index=2,
    containing_service=None,
    input_type=_FINDSUCCESSORREQUEST,
    output_type=_FINDSUCCESSORRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CHORDSERVICE)

DESCRIPTOR.services_by_name['ChordService'] = _CHORDSERVICE

# @@protoc_insertion_point(module_scope)
