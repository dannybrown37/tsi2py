from pathlib import Path
from pprint import pprint

from tsi2py.parser import parse_interfaces

import click


@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=False))
def main(path: click.Path) -> None:
    path = str(path)
    interfaces = parse_interfaces(path)
    pprint(interfaces)


if __name__ == '__main__':
    main()
