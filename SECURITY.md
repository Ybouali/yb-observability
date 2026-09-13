# Security Policy

## Supported Versions

Security fixes are provided for the latest released version of `yb-observability`.

| Version        | Supported |
| -------------- | --------- |
| Latest release | Yes       |
| Older releases | No        |

If you are using an older version, upgrade to the latest release before reporting an issue when possible.

## Reporting a Vulnerability

Please **do not report security vulnerabilities through public GitHub issues, pull requests, or discussions**.

Instead, report vulnerabilities privately to the project maintainer through GitHub's private security reporting mechanism.

When reporting a vulnerability, please include:

* A clear description of the vulnerability.
* The affected version.
* Steps to reproduce the issue.
* The potential security impact.
* Any relevant logs, code snippets, or proof-of-concept material.
* A suggested mitigation, if available.

Please provide enough information to reproduce and understand the issue without exposing sensitive information publicly.

## Responsible Disclosure

Please allow the maintainer reasonable time to investigate and address a reported vulnerability before publicly disclosing the issue.

The maintainer will:

1. Acknowledge the report when possible.
2. Investigate and validate the reported vulnerability.
3. Determine the affected versions and severity.
4. Prepare and release an appropriate fix.
5. Coordinate public disclosure when appropriate.

## Dependency Security

This project uses automated dependency monitoring to identify known vulnerabilities in its dependencies.

Security updates should be evaluated and applied as part of the project's normal maintenance process.

## Scope

This policy covers security vulnerabilities in:

* The `yb-observability` Python package.
* Code contained in this repository.
* Build and release configuration that could compromise package integrity.
* Dependencies where the project configuration directly introduces a security risk.

Issues unrelated to security should be reported through the project's normal GitHub issue or contribution process.

## Out of Scope

The following are generally outside the scope of this policy:

* Vulnerabilities in third-party services that are not caused by this project.
* Issues requiring an unsupported Python version.
* General bugs without a security impact.
* Social engineering attacks against project contributors or users.
* Denial-of-service testing against public infrastructure without prior authorization.

## Security Updates

Security fixes may be documented in the changelog and released through the project's normal release process.

Users should keep `yb-observability` updated to the latest supported release.
