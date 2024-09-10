from pathlib import Path
from pprint import pprint

from tsi2py.parser import parse_interfaces, convert_ts_enums_to_python
from tsi2py.serializer import serialize

import click


@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=False))
def main(path: click.Path) -> None:
    str_path = str(path)
    interfaces = parse_interfaces(str_path)
    enums = convert_ts_enums_to_python(str_path)
    serialized = serialize(interfaces, enums)
    print(serialized)


if __name__ == '__main__':
    main()
