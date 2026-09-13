# yb-observability

Reusable Python infrastructure for application configuration and observability.

`yb-observability` provides common infrastructure that can be shared across Python applications without coupling the library to a specific application or architecture.

The project currently focuses on configuration and logging, with additional observability capabilities planned for future releases.

## Features

### Configuration

* YAML configuration loading.
* Environment variable resolution.
* Nested environment variable support.
* Configuration validation.
* Clear configuration-related exceptions.

### Logging

* Loguru-based logging.
* Explicit application/service identity.
* Consistent human-readable log format.
* Console logging.
* File logging.
* Daily log rotation.
* Configurable retention.
* Per-service log directories.

### Future

The library is designed to grow with additional infrastructure such as:

* Structured/JSON logging.
* Request and correlation IDs.
* Metrics.
* Distributed tracing.
* OpenTelemetry integrations.
* Additional observability integrations.

Features are introduced incrementally and remain independent where possible.

## Installation

Install the package from PyPI:

```bash
pip install yb-observability
```

With `uv`:

```bash
uv add yb-observability
```

## Basic Usage

Configuration:

```python
from yb_observability.config import ConfigLoader

config = ConfigLoader("config.yml").load()
```

Logging:

```python
from yb_observability.logging import configure_logging

configure_logging(service="my-service")
```

The application remains responsible for deciding what should be logged. `yb-observability` is responsible for configuring the logging infrastructure and providing a consistent logging interface.

## Design Goals

### Reusable

The library must not depend on a specific application, framework, infrastructure provider, or domain.

### Explicit

Applications should explicitly configure the behavior they require rather than relying on hidden conventions.

### Consistent

Applications using the library should receive consistent configuration and logging behavior.

### Extensible

New capabilities should be possible without breaking the existing public API.

### Testable

Core functionality should be covered by automated tests.

### Production-oriented

The library should be suitable for both local development and production applications.

## Project Structure

```text
yb-observability/
├── src/
│   └── yb_observability/
│       ├── config/
│       └── logging/
│
├── tests/
│   ├── config/
│   └── logging/
│
├── docs/
│   ├── architecture/
│   ├── configuration/
│   └── logging/
│
├── .github/
│   └── workflows/
│
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
└── pyproject.toml
```

## Development

The project uses:

* Python 3.14
* uv
* Ruff
* Pyright
* Pytest
* Loguru
* PyYAML

Install development dependencies:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```

Run type checking:

```bash
uv run pyright
```

## Contributing

Contributions are welcome.

Before submitting a pull request, make sure that:

* Tests pass.
* Ruff checks pass.
* Formatting checks pass.
* Pyright checks pass.
* New functionality includes appropriate tests.
* Public API changes are documented.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and contribution guidelines.

## License

This project is licensed under the terms defined in [LICENSE](LICENSE).
