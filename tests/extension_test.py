from pathlib import Path

from tsi2py.parser import parse_interfaces
from tsi2py.serializer import serialize


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
        'Response<T>': {
            '__EXTENDS': ['Employee'],
            'data': 'T',
            'status': 'string',
        },
        'Supervisor': {
            '__EXTENDS': ['Person', 'Manager'],
            'supervisorId': 'number',
        },
    }


def test_serializer_with_extensions(data_path: Path) -> None:
    path = str(data_path / 'extends.ts')
    interfaces = parse_interfaces(path)
    serialized = serialize(interfaces)
    assert (
        serialized
        == """from typing import TypedDict, TypeVar, Literal, Generic, Any


T = TypeVar('T')


class Person(TypedDict):
    id: int
    name: str
    age: int


class Employee(TypedDict, Person):
    employeeId: int
    department: str


class Manager(TypedDict, Employee):
    teamSize: int
    managesDepartments: list[str]


class Supervisor(TypedDict, Person, Manager):
    supervisorId: int


class Response(TypedDict, Employee, Generic[T]):
    data: T
    status: str
"""
    )
