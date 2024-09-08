from pathlib import Path
from typing import Any

TYPE_MAPPING = {
    'string': 'str',
    'number': 'int',
    'boolean': 'bool',
    'Date': 'str',
    'T': 'Any',
    'null': 'None',
}


def convert_ts_type(ts_type: str | dict) -> str:
    """Convert TypeScript type to Python type."""
    if isinstance(ts_type, dict):
        return 'Any'
    if ts_type.endswith('[]'):
        return f'list[{TYPE_MAPPING.get(ts_type[:-2], ts_type[:-2])}]'
    return TYPE_MAPPING.get(ts_type, ts_type)


def generate_typed_dict(
    name: str,
    properties: dict[str, Any],
    processed: set,
    result: list,
) -> str:
    """Generate a Python TypedDict class definition from TS props."""
    if name in processed:
        return ''  # Skip if already processed

    processed.add(name)
    fields = []
    for key, value in properties.items():
        if isinstance(value, dict):
            nested_name = key.capitalize()
            fields.append(f'{key}: {nested_name}')
            nested_dict = generate_typed_dict(
                nested_name,
                value,
                processed,
                result,
            )
            result.append(nested_dict)
        else:
            python_type = convert_ts_type(value)
            fields.append(f'{key}: {python_type}')

    fields_str = '\n    '.join(fields)
    return f'class {name}(TypedDict):\n    {fields_str}\n'


def serialize(interfaces: dict[str, Any]) -> str:
    """Serialize a dictionary into a string of Python TypedDict classes."""

    # Generate TypedDict classes
    result = []
    processed = set()
    for name, properties in interfaces.items():
        typed_dict_name = name.replace('<T>', 'TypedDict')
        typed_dict_str = generate_typed_dict(
            typed_dict_name,
            properties,
            processed,
            result,
        )
        result.append(typed_dict_str)

    # Output to a file
    with Path('typed_dicts.py').open('w') as f:
        f.write('from typing import TypedDict, Generic, Any\n\n')
        f.write('\n'.join(result))

    print('TypedDict classes have been generated and saved to typed_dicts.py')
    return '\n'.join(result)
