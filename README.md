# tsi2py

Read TS interfaces from a `.ts` file and convert them into Python code.

## Installation

This is starting out mainly as a side project to get proficient with `uv`,
so using `uv` is recommended (until this is on PyPI and then I guess you
can do what you will).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the package locally and editably:

```bash
git clone https://github.com/dannybrown37/tsi2py.git
cd tsi2py
uv install -e .
```

## Usage

```bash
tsi2py <file_path>
```

This print some output to the console and will also write a `.py` file
to the same directory as the `.ts` file.

## Tests

Run the tests pretty easily with `pytest`:

```bash
pytest
```
