# Protocols

Messages in FIX rely on a protocol. This protocol describes the fields
and the structure of messages. As the protocol developed, new fields,
message types, and structural components were added, leading to different
versions. See below for an explanation of the message structure.

Although the protocol is a "standard", it is common that messages may be
altered, enriched, or new message types provided. When a FIX connection is
provided, both sides agree on the structure of the messages, and create a
common protocol.

## Loaders

This package provides two loaders: one for YAML formatted files, and one for
the QuickFIx XML format.

### YAML protocol files

The structure of the YAML files is given below. They are loaded in the following
manner.

```python
from jetblack_fixparser import load_yaml_protocol, ValueType

protocol = load_yaml_protocol(
    'FIX42.yaml',
    is_millisecond_time=True,
    is_float_decimal=True,
    is_type_enum={ ValueType.BOOLEAN: False }
)
```

The above example loaded the FIX 4.2 specification. It indicated that times
will include milliseconds, floats should be converted to decimals, and that
field of type `'BOOLEAN'` should not be converted to a text representation.


### XML protocol files

Due to the popularity of the [QuickFix](https://github.com/quickfix/quickfix)
engine, the XML format used by this product is widespread, and a loader is
provided. You can find the protocol files
[here](https://github.com/quickfix/quickfix/tree/master/spec).
They are loaded in the following manner.

```python
from jetblack_fixparser import load_quickfix_protocol, ValueType

protocol = load_quickfix_protocol(
    'FIX42.xml',
    is_millisecond_time=True,
    is_float_decimal=True,
    is_type_enum=None
)
```

See the YAML loader for a description of the arguments.

## Structure

This package comes with a set of protocol files in YAML format.

### Fields

Fields have a *type*, a *number*, and optionally a list fo *values* that
can give the raw value a readable meaning.

Here are a few example fields:

```yaml
fields:

  Account:
    number: 1
    type: STRING


  ExecTransType:
    number: 20
    type: CHAR
    values:
      0: NEW
      1: CANCEL
      2: CORRECT
      3: STATUS


  Price:
    number: 44
    type: PRICE
```

### Header

All messages start with a *header*. The header fields must be presented in
order. the order of other parts of the message may have more relaxed 
ordering constraints.

Here is an example header for FIX 4.0 (the most simple):

```yaml
header:
  BeginString:
    required: true
  BodyLength:
    required: true
  MsgType:
    required: true
  SenderCompID:
    required: true
  TargetCompID:
    required: true
  OnBehalfOfCompID:
  DeliverToCompID:
  SecureDataLen:
  SecureData:
  MsgSeqNum:
  SenderSubID:
  TargetSubID:
  OnBehalfOfSubID:
  DeliverToSubID:
  PossDupFlag:
  PossResend:
  SendingTime:
    required: true
  OrigSendingTime:
```

The header consists of a sequence of fields which may be *required*.

### Trailer

All messages end with a *trailer*.

Here is an example trailer:

```yaml
trailer:
  SignatureLength:
  Signature:
  CheckSum:
    required: true
```

### Messages

The messages themselves have a similar structure to header and trailer,
but with a message type and category.

Here is an example:

```yaml
messages:
  OrderCancelReject:
    msgtype: '9'
    msgcat: app
    fields:
      OrderID:
        required: true
      ClOrdID:
        required: true
      ClientID:
      ExecBroker:
      ListID:
      CxlRejReason:
      Text:
```
