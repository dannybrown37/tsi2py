from pathlib import Path

from tsi2py.parser import parse_interfaces


def test_parse_interfaces_with_extensions(data_path: Path) -> None:
    path = str(data_path / 'extends.ts')
    interfaces = parse_interfaces(path)
    assert interfaces == {
        'Employee': {
            '__EXTENDS': ['Person'],
            'department': 'string',
            'employeeId': 'number',
        },
        'Manager': {
            '__EXTENDS': ['Employee'],
            'managesDepartments': 'string[]',
            'teamSize': 'number',
        },
        'Person': {'age': 'number', 'id': 'number', 'name': 'string'},
        'Supervisor': {
            '__EXTENDS': ['Person', 'Manager'],
            'supervisorId': 'number',
        },
    }
