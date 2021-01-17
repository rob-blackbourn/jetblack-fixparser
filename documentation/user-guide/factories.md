# Factories

When two parties communicate over FIX they set and sender and target id which
never change. We can use a factory to simplify this.

To create a message using a factory:

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

