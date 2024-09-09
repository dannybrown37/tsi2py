from pathlib import Path

from tsi2py.parser import parse_interfaces
from tsi2py.serializer import serialize


def test_parser() -> None:
    path = str(Path(__file__).parent / 'interfaces' / 'sample.ts')
    interfaces = parse_interfaces(path)
    assert interfaces == {
        'APIResponse<T>': {
            'data': 'T',
            'message': 'string',
            'success': 'boolean',
        },
        'Config': {
            'debug': 'boolean',
            'env': '"development" | "production" | "test"',
            'maxRetries': 'number | null',
            'paths': {'logs': 'string', 'temp': 'string'},
            'version': 'number',
        },
        'Order': {
            'orderDate': 'Date',
            'orderId': 'number',
            'products': 'Product[]',
            'totalAmount': 'number',
            'userId': 'number',
        },
        'Product': {
            'available': 'boolean',
            'id': 'string',
            'name': 'string',
            'price': 'number',
            'tags': 'string[]',
        },
        'User': {
            'createdAt': 'Date',
            'email': 'string',
            'id': 'number',
            'isActive': 'boolean',
            'username': 'string',
        },
    }


def test_serializer() -> None:
    path = str(Path(__file__).parent / 'interfaces' / 'sample.ts')
    interfaces = parse_interfaces(path)
    serialized = serialize(interfaces)
    assert (
        serialized
        == """class User(TypedDict):
    id: int
    username: str
    email: str
    isActive: bool
    createdAt: str

class Product(TypedDict):
    id: str
    name: str
    price: int
    tags: list[str]
    available: bool

class Order(TypedDict):
    orderId: int
    userId: int
    products: list[Product]
    totalAmount: int
    orderDate: str

class APIResponseTypedDict(TypedDict):
    data: Any
    success: bool
    message: str

class Paths(TypedDict):
    logs: str
    temp: str

class Config(TypedDict):
    env: Literal["development"] | Literal["production"] | Literal["test"]
    debug: bool
    version: int
    paths: Paths
    maxRetries: int | None
"""
    )
