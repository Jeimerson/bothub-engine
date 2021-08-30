# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bothub/protos/inteligence/authentication.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='bothub/protos/inteligence/authentication.proto',
  package='weni.bothub.authentication',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n.bothub/protos/inteligence/authentication.proto\x12\x1aweni.bothub.authentication\x1a\x1bgoogle/protobuf/empty.proto\"G\n\x1dUserPermissionRetrieveRequest\x12\x16\n\x0eorg_user_email\x18\x01 \x01(\t\x12\x0e\n\x06org_id\x18\x02 \x01(\x05\"U\n\x1bUserPermissionUpdateRequest\x12\x0e\n\x06org_id\x18\x01 \x01(\x05\x12\x12\n\nuser_email\x18\x02 \x01(\t\x12\x12\n\npermission\x18\x03 \x01(\x05\"U\n\x1bUserPermissionRemoveRequest\x12\x0e\n\x06org_id\x18\x01 \x01(\x05\x12\x12\n\nuser_email\x18\x02 \x01(\t\x12\x12\n\npermission\x18\x03 \x01(\x05\"<\n\x19UserLanguageUpdateRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08language\x18\x02 \x01(\t\"\x1a\n\nPermission\x12\x0c\n\x04role\x18\x01 \x01(\x05\"$\n\x13UserRetrieveRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"\x8f\x01\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x10\n\x08language\x18\x05 \x01(\t\x12\x11\n\tjoined_at\x18\x06 \x01(\t\x12\x11\n\tis_active\x18\x07 \x01(\x08\x12\x14\n\x0cis_superuser\x18\x08 \x01(\x08\x32\xd5\x02\n\x18UserPermissionController\x12o\n\x08Retrieve\x12\x39.weni.bothub.authentication.UserPermissionRetrieveRequest\x1a&.weni.bothub.authentication.Permission\"\x00\x12k\n\x06Update\x12\x37.weni.bothub.authentication.UserPermissionUpdateRequest\x1a&.weni.bothub.authentication.Permission\"\x00\x12[\n\x06Remove\x12\x37.weni.bothub.authentication.UserPermissionRemoveRequest\x1a\x16.google.protobuf.Empty\"\x00\x32q\n\x0eUserController\x12_\n\x08Retrieve\x12/.weni.bothub.authentication.UserRetrieveRequest\x1a .weni.bothub.authentication.User\"\x00\x32}\n\x16UserLanguageController\x12\x63\n\x06Update\x12\x35.weni.bothub.authentication.UserLanguageUpdateRequest\x1a .weni.bothub.authentication.User\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_USERPERMISSIONRETRIEVEREQUEST = _descriptor.Descriptor(
  name='UserPermissionRetrieveRequest',
  full_name='weni.bothub.authentication.UserPermissionRetrieveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='org_user_email', full_name='weni.bothub.authentication.UserPermissionRetrieveRequest.org_user_email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='org_id', full_name='weni.bothub.authentication.UserPermissionRetrieveRequest.org_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=178,
)


_USERPERMISSIONUPDATEREQUEST = _descriptor.Descriptor(
  name='UserPermissionUpdateRequest',
  full_name='weni.bothub.authentication.UserPermissionUpdateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='org_id', full_name='weni.bothub.authentication.UserPermissionUpdateRequest.org_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_email', full_name='weni.bothub.authentication.UserPermissionUpdateRequest.user_email', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='permission', full_name='weni.bothub.authentication.UserPermissionUpdateRequest.permission', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=180,
  serialized_end=265,
)


_USERPERMISSIONREMOVEREQUEST = _descriptor.Descriptor(
  name='UserPermissionRemoveRequest',
  full_name='weni.bothub.authentication.UserPermissionRemoveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='org_id', full_name='weni.bothub.authentication.UserPermissionRemoveRequest.org_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_email', full_name='weni.bothub.authentication.UserPermissionRemoveRequest.user_email', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='permission', full_name='weni.bothub.authentication.UserPermissionRemoveRequest.permission', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=267,
  serialized_end=352,
)


_USERLANGUAGEUPDATEREQUEST = _descriptor.Descriptor(
  name='UserLanguageUpdateRequest',
  full_name='weni.bothub.authentication.UserLanguageUpdateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='weni.bothub.authentication.UserLanguageUpdateRequest.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='language', full_name='weni.bothub.authentication.UserLanguageUpdateRequest.language', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=354,
  serialized_end=414,
)


_PERMISSION = _descriptor.Descriptor(
  name='Permission',
  full_name='weni.bothub.authentication.Permission',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='role', full_name='weni.bothub.authentication.Permission.role', index=0,
      number=1, type=5, cpp_type=1, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=416,
  serialized_end=442,
)


_USERRETRIEVEREQUEST = _descriptor.Descriptor(
  name='UserRetrieveRequest',
  full_name='weni.bothub.authentication.UserRetrieveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='weni.bothub.authentication.UserRetrieveRequest.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=444,
  serialized_end=480,
)


_USER = _descriptor.Descriptor(
  name='User',
  full_name='weni.bothub.authentication.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='weni.bothub.authentication.User.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='email', full_name='weni.bothub.authentication.User.email', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='weni.bothub.authentication.User.nickname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='weni.bothub.authentication.User.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='language', full_name='weni.bothub.authentication.User.language', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='joined_at', full_name='weni.bothub.authentication.User.joined_at', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_active', full_name='weni.bothub.authentication.User.is_active', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_superuser', full_name='weni.bothub.authentication.User.is_superuser', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=483,
  serialized_end=626,
)

DESCRIPTOR.message_types_by_name['UserPermissionRetrieveRequest'] = _USERPERMISSIONRETRIEVEREQUEST
DESCRIPTOR.message_types_by_name['UserPermissionUpdateRequest'] = _USERPERMISSIONUPDATEREQUEST
DESCRIPTOR.message_types_by_name['UserPermissionRemoveRequest'] = _USERPERMISSIONREMOVEREQUEST
DESCRIPTOR.message_types_by_name['UserLanguageUpdateRequest'] = _USERLANGUAGEUPDATEREQUEST
DESCRIPTOR.message_types_by_name['Permission'] = _PERMISSION
DESCRIPTOR.message_types_by_name['UserRetrieveRequest'] = _USERRETRIEVEREQUEST
DESCRIPTOR.message_types_by_name['User'] = _USER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserPermissionRetrieveRequest = _reflection.GeneratedProtocolMessageType('UserPermissionRetrieveRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERPERMISSIONRETRIEVEREQUEST,
  '__module__' : 'bothub.protos.inteligence.authentication_pb2'
  # @@protoc_insertion_point(class_scope:weni.bothub.authentication.UserPermissionRetrieveRequest)
  })
_sym_db.RegisterMessage(UserPermissionRetrieveRequest)

UserPermissionUpdateRequest = _reflection.GeneratedProtocolMessageType('UserPermissionUpdateRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERPERMISSIONUPDATEREQUEST,
  '__module__' : 'bothub.protos.inteligence.authentication_pb2'
  # @@protoc_insertion_point(class_scope:weni.bothub.authentication.UserPermissionUpdateRequest)
  })
_sym_db.RegisterMessage(UserPermissionUpdateRequest)

UserPermissionRemoveRequest = _reflection.GeneratedProtocolMessageType('UserPermissionRemoveRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERPERMISSIONREMOVEREQUEST,
  '__module__' : 'bothub.protos.inteligence.authentication_pb2'
  # @@protoc_insertion_point(class_scope:weni.bothub.authentication.UserPermissionRemoveRequest)
  })
_sym_db.RegisterMessage(UserPermissionRemoveRequest)

UserLanguageUpdateRequest = _reflection.GeneratedProtocolMessageType('UserLanguageUpdateRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERLANGUAGEUPDATEREQUEST,
  '__module__' : 'bothub.protos.inteligence.authentication_pb2'
  # @@protoc_insertion_point(class_scope:weni.bothub.authentication.UserLanguageUpdateRequest)
  })
_sym_db.RegisterMessage(UserLanguageUpdateRequest)

Permission = _reflection.GeneratedProtocolMessageType('Permission', (_message.Message,), {
  'DESCRIPTOR' : _PERMISSION,
  '__module__' : 'bothub.protos.inteligence.authentication_pb2'
  # @@protoc_insertion_point(class_scope:weni.bothub.authentication.Permission)
  })
_sym_db.RegisterMessage(Permission)

UserRetrieveRequest = _reflection.GeneratedProtocolMessageType('UserRetrieveRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERRETRIEVEREQUEST,
  '__module__' : 'bothub.protos.inteligence.authentication_pb2'
  # @@protoc_insertion_point(class_scope:weni.bothub.authentication.UserRetrieveRequest)
  })
_sym_db.RegisterMessage(UserRetrieveRequest)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'bothub.protos.inteligence.authentication_pb2'
  # @@protoc_insertion_point(class_scope:weni.bothub.authentication.User)
  })
_sym_db.RegisterMessage(User)



_USERPERMISSIONCONTROLLER = _descriptor.ServiceDescriptor(
  name='UserPermissionController',
  full_name='weni.bothub.authentication.UserPermissionController',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=629,
  serialized_end=970,
  methods=[
  _descriptor.MethodDescriptor(
    name='Retrieve',
    full_name='weni.bothub.authentication.UserPermissionController.Retrieve',
    index=0,
    containing_service=None,
    input_type=_USERPERMISSIONRETRIEVEREQUEST,
    output_type=_PERMISSION,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Update',
    full_name='weni.bothub.authentication.UserPermissionController.Update',
    index=1,
    containing_service=None,
    input_type=_USERPERMISSIONUPDATEREQUEST,
    output_type=_PERMISSION,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Remove',
    full_name='weni.bothub.authentication.UserPermissionController.Remove',
    index=2,
    containing_service=None,
    input_type=_USERPERMISSIONREMOVEREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERPERMISSIONCONTROLLER)

DESCRIPTOR.services_by_name['UserPermissionController'] = _USERPERMISSIONCONTROLLER


_USERCONTROLLER = _descriptor.ServiceDescriptor(
  name='UserController',
  full_name='weni.bothub.authentication.UserController',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=972,
  serialized_end=1085,
  methods=[
  _descriptor.MethodDescriptor(
    name='Retrieve',
    full_name='weni.bothub.authentication.UserController.Retrieve',
    index=0,
    containing_service=None,
    input_type=_USERRETRIEVEREQUEST,
    output_type=_USER,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERCONTROLLER)

DESCRIPTOR.services_by_name['UserController'] = _USERCONTROLLER


_USERLANGUAGECONTROLLER = _descriptor.ServiceDescriptor(
  name='UserLanguageController',
  full_name='weni.bothub.authentication.UserLanguageController',
  file=DESCRIPTOR,
  index=2,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1087,
  serialized_end=1212,
  methods=[
  _descriptor.MethodDescriptor(
    name='Update',
    full_name='weni.bothub.authentication.UserLanguageController.Update',
    index=0,
    containing_service=None,
    input_type=_USERLANGUAGEUPDATEREQUEST,
    output_type=_USER,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERLANGUAGECONTROLLER)

DESCRIPTOR.services_by_name['UserLanguageController'] = _USERLANGUAGECONTROLLER

# @@protoc_insertion_point(module_scope)
