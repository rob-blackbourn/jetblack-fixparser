# jetblack-fixparser

A parser for FIX messages.

## Installation

The package can be installed with `pip`.

```bash
pip install jetblack-fixparser
```

## Protocol Files

While FIX is a standard, the structure of the fields and messages is configurable.
This configuration is typically loaded from a file. The source repository
contains a number of such files in the `/etc` folder in `YAML` format. There is
also a *QuickFix* loader.

The YAML format makes use of defaults. All message fields default to type `field`,
so only `group` and `component` fields need to be explicitly specified. Also all
message fields are consider optional, non-optional fields must be marked as
`required: true`.

## Usage

### Decoding

To decode a FIX bytes buffer -

```python
from jetblack_fixparser import load_yaml_protocol, FixMessage

buffer = b'8=FIX.4.4|9=94|35=3|49=A|56=AB|128=B1|34=214|50=U1|52=20100304-09:42:23.130|45=176|371=15|372=X|373=1|58=txt|10=058|',

protocol = load_yaml_protocol(
    'FIX44.yaml',
    is_millisecond_time=True,
    is_float_decimal=True
)

fix_message = FixMessage.decode(
    protocol,
    buffer,
    sep=b'|',
    strict=True,
    validate=True,
    convert_sep_for_checksum=True
)

print(fix_message.message)
```

Note that strict validation is enabled. This ensures all required fields are
specified. Also the separator is changed from `NULL` to `|` to so they can be
displayed. However the checksum was calculated with the original field separator
so the `convert_sep_for_checksum` is set to `true`.

### Encoding

To encode a dictionary describing a FIX message - 

```python
from datetime import datetime, timezone
from jetblack_fixparser import load_yaml_protocol, FixMessage

protocol = load_yaml_protocol(
    'FIX44.yaml',
    is_millisecond_time=True,
    is_float_decimal=True,
    is_type_enum=None
)
sending_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=timezone.utc)

fix_message = FixMessage(
    protocol,
    {
        'MsgType': 'LOGON',
        'MsgSeqNum': 42,
        'SenderCompID': "SENDER",
        'TargetCompID': "TARGET",
        'SendingTime': sending_time,
        'EncryptMethod': "NONE",
        'HeartBtInt': 30
    }
)
buffer = fix_message.encode(regenerate_integrity=True)

print(buffer)
```

Note that the `BeginString`, `BodyLength` and `Checksum` fields were automatically
generated.

### Factories

To encode and decode a message using a factory - 

```python
from datetime import datetime, timezone
from jetblack_fixparser import load_yaml_protocol, FixMessage, FixMessageFactory

protocol = load_yaml_protocol(
    'FIX44.yaml',
    is_millisecond_time=True,
    is_float_decimal=True,
    is_type_enum=None
)

factory = FixMessageFactory(protocol, "SENDER", "TARGET")

sending_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
fix_messages = factory.create(
        'LOGON',
        42,
        sending_time,
        {
            'EncryptMethod': "NONE",
            'HeartBtInt': 30
        }
    )

buffer = fix_message.encode(regenerate_integrity=True)
roundtrip = FixMessage.decode(protocol, buffer)
assert fix_message.message == roundtrip.message
```

Because the sender and target remain the same, we can simplify message generation
with the factory.
