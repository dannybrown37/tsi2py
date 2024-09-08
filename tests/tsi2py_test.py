from pathlib import Path

from tsi2py.parser import parse_interfaces


INTERFACE_COUNT_IN_SAMPLE_FILE = 5


def test_parser() -> None:
    path = str(Path(__file__).parent / 'interfaces' / 'sample.ts')
    print(path)
    interfaces = parse_interfaces(path)
    print(interfaces)
    assert len(interfaces) == INTERFACE_COUNT_IN_SAMPLE_FILE
