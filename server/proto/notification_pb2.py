# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server/proto/notification.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fserver/proto/notification.proto\"v\n\x10\x45mailSendRequest\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0f\n\x07subject\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x0e\n\x06groups\x18\x04 \x03(\t\x12\x10\n\x08\x61\x63\x63ounts\x18\x05 \x03(\t\x12\x0e\n\x06\x65mails\x18\x06 \x03(\t\"\x94\x01\n\x11\x45mailSendResponse\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0e\n\x06sender\x18\x02 \x01(\t\x12\x0f\n\x07subject\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\x1e\n\nrecipients\x18\x06 \x03(\x0b\x32\n.Recipient\x12\x11\n\ttimestamp\x18\x07 \x01(\x02\"(\n\x15SimpleMessageResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"6\n\tRecipient\x12\r\n\x05group\x18\x01 \x01(\t\x12\x1a\n\x08\x61\x63\x63ounts\x18\x02 \x03(\x0b\x32\x08.Account\"8\n\x07\x41\x63\x63ount\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\xb0\x01\n\x13NotifyCreateRequest\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0f\n\x07subject\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x10\n\x08is_email\x18\x04 \x01(\x08\x12\x12\n\nis_message\x18\x05 \x01(\x08\x12\x0f\n\x07is_line\x18\x06 \x01(\x08\x12\x0e\n\x06groups\x18\x07 \x03(\t\x12\x10\n\x08\x61\x63\x63ounts\x18\x08 \x03(\t\x12\x0e\n\x06\x65mails\x18\t \x03(\t\"\xdb\x01\n\x0eNotifyResponse\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0e\n\x06sender\x18\x02 \x01(\t\x12\x0f\n\x07subject\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\t\x12\x10\n\x08is_email\x18\x05 \x01(\x08\x12\x12\n\nis_message\x18\x06 \x01(\x08\x12\x0f\n\x07is_line\x18\x07 \x01(\x08\x12\x14\n\x0c\x65mail_result\x18\x08 \x01(\x08\x12\x16\n\x0emessage_result\x18\t \x01(\x08\x12\x13\n\x0bline_result\x18\n \x01(\x08\x12\x11\n\ttimestamp\x18\x0b \x01(\x02\x32\xfe\x01\n\x13NotificationService\x12\x32\n\tSendEmail\x12\x11.EmailSendRequest\x1a\x12.EmailSendResponse\x12<\n\x0fSendEmailSimple\x12\x11.EmailSendRequest\x1a\x16.SimpleMessageResponse\x12\x33\n\nSendNotify\x12\x14.NotifyCreateRequest\x1a\x0f.NotifyResponse\x12@\n\x10SendNotifySimple\x12\x14.NotifyCreateRequest\x1a\x16.SimpleMessageResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'server.proto.notification_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMAILSENDREQUEST']._serialized_start=35
  _globals['_EMAILSENDREQUEST']._serialized_end=153
  _globals['_EMAILSENDRESPONSE']._serialized_start=156
  _globals['_EMAILSENDRESPONSE']._serialized_end=304
  _globals['_SIMPLEMESSAGERESPONSE']._serialized_start=306
  _globals['_SIMPLEMESSAGERESPONSE']._serialized_end=346
  _globals['_RECIPIENT']._serialized_start=348
  _globals['_RECIPIENT']._serialized_end=402
  _globals['_ACCOUNT']._serialized_start=404
  _globals['_ACCOUNT']._serialized_end=460
  _globals['_NOTIFYCREATEREQUEST']._serialized_start=463
  _globals['_NOTIFYCREATEREQUEST']._serialized_end=639
  _globals['_NOTIFYRESPONSE']._serialized_start=642
  _globals['_NOTIFYRESPONSE']._serialized_end=861
  _globals['_NOTIFICATIONSERVICE']._serialized_start=864
  _globals['_NOTIFICATIONSERVICE']._serialized_end=1118
# @@protoc_insertion_point(module_scope)
