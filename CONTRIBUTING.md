# Contributing to yb-observability

Thank you for contributing to `yb-observability`.

The project is designed as a reusable Python library, so contributions should prioritize clear APIs, minimal coupling, backwards compatibility, and strong test coverage.

## Development Requirements

The project currently uses:

* Python 3.14
* uv
* Pytest
* Ruff
* Pyright

Clone the repository and enter the project:

```bash
git clone <repository-url>
cd yb-observability
```

Install the development environment:

```bash
uv sync
```

## Project Structure

```text
src/yb_observability/
├── config/
└── logging/

tests/
├── config/
└── logging/
```

Implementation code belongs under `src/yb_observability/`.

Tests belong under the corresponding directory in `tests/`.

For example:

```text
src/yb_observability/config/loader.py
tests/config/test_loader.py
```

## Development Workflow

Create a branch for your work:

```bash
git switch -c feature/my-feature
```

Make the changes and add tests where appropriate.

Run the complete test suite:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```

Run Pyright:

```bash
uv run pyright
```

All checks should pass before opening a pull request.

## Code Style

Follow the project's Ruff configuration.

The project uses:

* 88-character line length.
* Double quotes.
* Four spaces for indentation.
* Python 3.14 syntax and typing features where appropriate.

Prefer simple and explicit implementations over unnecessary abstractions.

## Public API

Changes to the public API should be made carefully.

Before adding a public class, function, or module, consider whether it is genuinely useful to library consumers.

Avoid exposing implementation details unnecessarily.

For example, prefer a stable public API such as:

```python
from yb_observability.config import ConfigLoader
```

rather than requiring consumers to import internal implementation modules.

## Tests

New functionality should include tests.

Tests should verify observable behavior rather than implementation details.

For bug fixes, add a regression test whenever practical.

The test suite can be run with:

```bash
uv run pytest
```

## Documentation

Public functionality should be documented.

Documentation should explain:

* What the feature does.
* Why it exists.
* How to use it.
* Important configuration or behavioral constraints.

Architectural decisions should be documented separately when they affect the design of the library.

## Commit Messages

Use clear, descriptive commit messages.

The project follows Conventional Commits.

Examples:

```text
feat(config): add environment variable resolution
fix(config): handle invalid YAML
feat(logging): add daily file rotation
test(config): add nested environment tests
docs(logging): document retention configuration
refactor(logging): simplify handler configuration
```

Common commit types include:

```text
feat
fix
docs
test
refactor
chore
ci
```

## Pull Requests

Pull requests should:

* Explain what changed.
* Explain why the change was needed.
* Include tests for new behavior.
* Keep unrelated changes out of the pull request.
* Pass all automated checks.

Keep pull requests focused. A feature, bug fix, or refactor should normally be submitted separately rather than combining unrelated changes.

## Backwards Compatibility

`yb-observability` is a reusable library, so backwards compatibility is important.

Breaking changes to public APIs should:

1. Be clearly identified.
2. Be documented.
3. Include an appropriate version change.
4. Explain the migration path when possible.

The project follows semantic versioning:

```text
MAJOR.MINOR.PATCH
```

For example:

```text
0.1.0
0.2.0
0.2.1
```

While the project remains below `1.0.0`, the public API may evolve more quickly, but breaking changes should still be intentional and documented.

## Issues

Before opening an issue:

* Search existing issues.
* Verify that the behavior is reproducible.
* Include relevant error messages and environment information.
* Provide a minimal reproduction when reporting a bug.

Do not include secrets, credentials, API keys, or other sensitive information in issues.

## Security Issues

Do not report security vulnerabilities through public GitHub issues.

See `SECURITY.md` for the security reporting process.

## Code of Conduct

All contributors are expected to follow the project's `CODE_OF_CONDUCT.md`.

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

`yb-observability` is distributed under the MIT License.
