from pathlib import Path

from tsi2py.parser import parse_interfaces


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
