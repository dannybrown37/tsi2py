from pathlib import Path
from pprint import pprint

from tsi2py.parser import parse_interfaces

import click


@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=False))
def main(path: click.Path) -> None:
    with Path(str(path)).open('r') as f:
        data = f.read()
    interfaces = parse_interfaces(data)
    pprint(interfaces)


if __name__ == '__main__':
    main()
