# LLaMArch
[![Downloads](https://pepy.tech/badge/llamarch)](https://pepy.tech/project/llamarch)

Building Block Architectures for GenAI

## Installation

```bash
pip install llamarch
```

## Usage

```python
from llamarch import ...
```

## Contributing

Contributions are welcome! Please read the [contribution guidelines](CONTRIBUTING.md) first.

## How to get coverage?

To get coverage, execute the following command from the parent folder:
```
python -m pytest --cov=llamarch --cov-report <option> tests
```

The `option` can be related to showing covered/missed lines or specifying the output format of the report. For example, to get a line-by-line report, use the following command:
```
python -m pytest --cov=llamarch --cov-report term-missing tests
```

## Whom to contact?

Please direct your queries to [gpavanb1](http://github.com/gpavanb1)
for any questions.
