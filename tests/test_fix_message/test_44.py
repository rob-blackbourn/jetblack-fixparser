"""Test for decoding"""

from jetblack_fixparser.loader import load_yaml_protocol
from jetblack_fixparser.fix_message import FixMessage


def test_messages():
    """Test decoding messages"""
    messages = [
        b'8=FIX.4.4|9=94|35=3|49=A|56=AB|128=B1|34=214|50=U1|52=20100304-09:42:23.130|45=176|371=15|372=X|373=1|58=txt|10=058|',
        b'8=FIX.4.4|9=117|35=AD|49=A|56=B|34=2|50=1|57=M|52=20100219-14:33:32.258|568=1|569=0|263=1|580=1|75=20100218|60=20100218-00:00:00.000|10=202|',
        b'8=FIX.4.4|9=122|35=D|49=CLIENT12|56=B|34=215|52=20100225-19:41:57.316|11=13346|1=Marcel|21=1|54=1|60=20100225-19:39:52.020|40=2|44=5|59=0|10=072|',

    ]

    protocol = load_yaml_protocol(
        'etc/FIX44.yaml',
        is_millisecond_time=True,
        is_float_decimal=True
    )

    for buf in messages:
        msg = FixMessage.decode(
            protocol, buf, sep=b'|', strict=True, validate=True, convert_sep_for_checksum=True)
        round_trip = msg.encode(
            sep=b'|', regenerate_integrity=True, convert_sep_for_checksum=True)
        assert buf == round_trip
