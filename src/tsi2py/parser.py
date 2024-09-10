import re
from pathlib import Path
from pprint import pprint


def convert_ts_enums_to_python(file_path: str) -> str:
    ts_enum_pattern = re.compile(r'enum\s+(\w+)\s*{([^}]+)}', re.MULTILINE)
    enum_value_pattern = re.compile(r'(\w+)\s*=\s*["\']?(\w+)["\']?')

    with Path(file_path).open('r') as ts_file:
        ts_content = ts_file.read()

    python_enums = []
    matches = ts_enum_pattern.findall(ts_content)

    for match in matches:
        enum_name, enum_body = match
        enum_body = [e.strip() for e in enum_body.split(',')]
        python_enum = f'class {enum_name}(Enum):\n'
        for enum_member in enum_body:
            if enum_member:
                value_match = enum_value_pattern.search(enum_member)
                if value_match:
                    member_name, member_value = value_match.groups()
                else:
                    member_name = enum_member
                    member_value = enum_member
                python_enum += f"    {member_name} = '{member_value}'\n"
        python_enums.append(python_enum)

    return '\n\n'.join(python_enums)


def find_interfaces(text: str) -> list:
    regex = r'interface\s+(\w+)(<\w+>)?\s*(extends\s+[\w\s,]+)?\s*{'
    interface_pattern = re.compile(regex)
    interfaces = []

    for match in interface_pattern.finditer(text):
        interface_name = match.group(1)
        generic_type = match.group(2)
        extended_interface = (
            match.group(3).replace('extends', '').strip()
            if match.group(3)
            else None
        )
        start_index = match.end()
        brace_count = 1
        i = start_index

        while brace_count > 0 and i < len(text):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
            i += 1

        interface_body = text[start_index : i - 1].strip()
        interfaces.append(
            (
                interface_name,
                generic_type,
                interface_body,
                extended_interface,
            ),
        )

    return interfaces


def parse_interfaces(file_path: str) -> dict:  # noqa: C901
    with Path(file_path).open('r') as f:
        file_content = f.read()
    print(f'File {file_path} contents have been read:\n\n', file_content)
    interfaces = {}
    matches = find_interfaces(file_content)
    for match in matches:
        interface_name = match[0]
        generic_type = match[1] if match[1] else None
        interface_body = match[2]
        extended_interfaces = match[3] if match[3] else None

        attributes = {}
        nested_object = {}
        nested_object_key = None

        if extended_interfaces:
            extends = [e.strip() for e in extended_interfaces.split(',')]
            attributes['__EXTENDS'] = extends

        for body_line in interface_body.splitlines():
            line = body_line.strip()
            if not line:
                continue

            # Detect and handle nested objects
            if '{' in line:
                nested_object_key = re.match(r'(\w+)\s*:\s*{', line)
                if not nested_object_key:
                    msg = f'Invalid line: {line}'
                    raise ValueError(msg)
                nested_object_key = nested_object_key.group(1)
                nested_object = {}
                attributes[nested_object_key] = nested_object
                continue

            if '}' in line:
                attributes[nested_object_key] = nested_object
                nested_object_key = None
                continue

            # Key-value pair within a nested object
            if nested_object_key:
                attr_match = re.match(r'(\w+)\s*:\s*([^;]+);', line)
                if attr_match:
                    attr_name = attr_match.group(1)
                    attr_type = attr_match.group(2).strip()
                    nested_object[attr_name] = attr_type
                continue

            # Normal key-value pair
            attr_match = re.match(r'(\w+)\s*:\s*(.+?);', line)
            if attr_match:
                attr_name = attr_match.group(1)
                attr_type = attr_match.group(2).strip()
                attributes[attr_name] = attr_type

        # If it's a generic interface, include the generic type in the key
        if generic_type:
            interface_name += generic_type

        interfaces[interface_name] = attributes

    return interfaces


if __name__ == '__main__':
    file = Path(__file__).parents[2] / 'tests' / 'interfaces' / 'extends.ts'
    pprint(parse_interfaces(str(file)))

    file = file.parent / 'enum.ts'
    pprint(convert_ts_enums_to_python(str(file)))
