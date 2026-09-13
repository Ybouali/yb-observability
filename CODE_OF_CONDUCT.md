# Security Policy

## Supported Versions

Security fixes are generally applied to actively maintained versions of `yb-observability`.

| Version              | Supported   |
| -------------------- | ----------- |
| Latest minor release | Yes         |
| Older releases       | Best effort |
| Unsupported releases | No          |

Users should keep `yb-observability` up to date whenever possible.

## Reporting a Vulnerability

Please do **not** report security vulnerabilities through public GitHub issues.

If you believe you have found a security vulnerability, report it privately through the repository's GitHub security reporting mechanism.

When reporting a vulnerability, include:

* A clear description of the vulnerability.
* The affected version.
* Steps required to reproduce the issue.
* The potential security impact.
* Any relevant logs, stack traces, or proof of concept that can safely be shared.

Please do not include secrets, credentials, API keys, personal data, or other sensitive information in the report.

## Responsible Disclosure

Please allow reasonable time for the vulnerability to be investigated and addressed before publicly disclosing technical details.

Security fixes may be released as a patch, minor release, or major release depending on the impact and whether the change affects the public API.

## Dependency Security

The project depends on third-party Python packages.

Dependencies should be kept reasonably up to date, and security-related dependency updates should be addressed promptly when practical.

Contributors should avoid introducing dependencies when the functionality can be implemented safely without adding unnecessary project complexity.

## Scope

This policy covers security vulnerabilities in:

* `yb-observability` source code.
* Build and packaging configuration.
* Project infrastructure that can affect users of the published package.
* Dependencies introduced directly by the project where the project configuration is responsible for the vulnerability.

Application-specific security issues in software that uses `yb-observability` should be reported to the maintainers of that application.
