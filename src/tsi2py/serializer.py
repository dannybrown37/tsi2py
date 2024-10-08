from pathlib import Path
from typing import Any


TYPE_MAPPING = {
    'string': 'str',
    'number': 'int',
    'boolean': 'bool',
    'Date': 'str',
    'null': 'None',
}


def convert_ts_type(ts_type: str | dict) -> str:
    """Convert TypeScript type to Python type."""
    if isinstance(ts_type, dict):
        return 'Any'
    if '|' in ts_type:
        return ' | '.join(
            convert_ts_type(t.strip()) for t in ts_type.split('|')
        )
    if "'" in ts_type or '"' in ts_type:
        return f'Literal[{ts_type}]'
    if ts_type.endswith('[]'):
        return f'list[{TYPE_MAPPING.get(ts_type[:-2], ts_type[:-2])}]'
    return TYPE_MAPPING.get(ts_type, ts_type)


def generate_typed_dict_str(
    name: str,
    properties: dict[str, Any],
    processed: set,
    result: list,
    generic: str | None = None,
) -> str:
    """Generate a Python TypedDict class definition from TS props."""
    if name in processed:
        return ''  # Skip if already processed

    processed.add(name)
    extensions = None
    fields = []
    for key, value in properties.items():
        if isinstance(value, dict):
            nested_name = key.capitalize()
            fields.append(f'{key}: {nested_name}')
            nested_dict = generate_typed_dict_str(
                nested_name,
                value,
                processed,
                result,
            )
            result.append(nested_dict)
        elif key == '__EXTENDS':
            extensions = ', '.join(value)
        else:
            python_type = convert_ts_type(value)
            fields.append(f'{key}: {python_type}')

    fields_str = '\n    '.join(fields)
    if extensions and generic:
        return f'class {name}(TypedDict, {extensions}, Generic[{generic}]):\n    {fields_str}\n'  # noqa: E501
    if extensions:
        return f'class {name}(TypedDict, {extensions}):\n    {fields_str}\n'
    if generic:
        return (
            f'class {name}(TypedDict, Generic[{generic}]):\n    {fields_str}\n'
        )
    return f'class {name}(TypedDict):\n    {fields_str}\n'


def serialize_file(
    interfaces: dict[str, Any],
    enums: str | None = None,
) -> str:
    """Serialize a dictionary into a string of Python TypedDict classes."""

    # Generate TypedDict classes
    result = []
    generics = []
    processed = set()
    for name, properties in interfaces.items():
        generic = None
        if '<' in name and '>' in name:
            typed_dict_name = name.split('<')[0].strip()
            generic = name.split('<')[1].split('>')[0].strip()
            generics.append(generic)
        else:
            typed_dict_name = name
        typed_dict_str = generate_typed_dict_str(
            typed_dict_name,
            properties,
            processed,
            result,
            generic,
        )
        result.append(typed_dict_str)

    enum_import = 'from enum import Enum\n' if enums else ''
    head = 'from typing import TypedDict, TypeVar, Literal, Generic, Any\n\n\n'
    generics = ''.join([f"{g} = TypeVar('{g}')\n" for g in generics]) + '\n\n'
    enums = f'{enums}\n\n' if enums else ''
    result = '\n\n'.join(result)
    output = f'{enum_import}{head}{generics}{enums}{result}'

    # Output to a file
    with Path('typed_dicts.py').open('w') as f:
        f.write(output)

    print('\nTypedDicts have been generated from interfaces and saved\n\n')
    return output
