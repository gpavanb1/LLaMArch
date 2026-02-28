# LLaMArch
[![Downloads](https://pepy.tech/badge/llamarch)](https://pepy.tech/project/llamarch)

Minimal, Building Blocks for Large Language Models!

## Installation

```bash
pip install llamarch
```

## Usage

```python
from llamarch import ...
```

## Testing

To run the tests, first install the test dependencies:

```bash
pip install pytest
```

The tests require several services (Neo4j, Redis, Qdrant) to be running. You can use the provided `docker-compose.yml` to start these services:

```bash
docker compose up -d
```

Then run the tests using:

```bash
pytest
```

Alternatively, you can use the provided test script which starts the services, runs the tests, and then shuts down the services:

```bash
./scripts/run_tests.sh
```

Refer to the [documentation site](https://gpavanb1.github.io/llamarch-docs/) for more information.

## Whom to contact?

Please direct your queries to [gpavanb1](http://github.com/gpavanb1)
for any questions.

You can raise any issues faced while using the project at this [link](https://github.com/gpavanb1/llamarch-docs/issues)

## How to create documentation?

The documentation is generated using [mkdocs](https://www.mkdocs.org/). Local version can be viewed using `mkdocs serve` and the deployment is done using
```
mkdocs gh-deploy
```
