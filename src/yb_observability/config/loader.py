from os import getenv
from pathlib import Path
from re import Match, compile
from typing import Any

from yaml import YAMLError, safe_load

from yb_observability.config.exceptions import (
    ConfigEnvironmentVariableError,
    ConfigFileNotFoundError,
    ConfigLoaderError,
)

_ENV_VAR_PATTERN = compile(r"\$\{([A-Za-z][A-Za-z0-9_]*)\}")


class ConfigLoader:
    """Load YAML configuration and resolve environment variables."""

    def __init__(self, config_path: str | Path) -> None:
        self.config_path = Path(config_path)

    def load(self) -> dict[str, Any]:
        """Load and resolve the configuration file."""

        if not self.config_path.is_file():
            raise ConfigFileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            content = self.config_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ConfigLoaderError(
                f"Unable to read configuration file: {self.config_path}"
            ) from exc

        resolved_content = self._resolve_environment_variables(content)

        try:
            config = safe_load(resolved_content)
        except YAMLError as exc:
            raise ConfigLoaderError(
                f"Invalid YAML configuration: {self.config_path}"
            ) from exc

        if config is None:
            return {}

        if not isinstance(config, dict):
            raise ConfigLoaderError(
                "The root of the configuration file must be a YAML mapping."
            )

        return config

    @staticmethod
    def _resolve_environment_variables(content: str) -> str:
        """Resolve ${ENV_VAR} references using environment variables."""

        def replace(match: Match[str]) -> str:
            variable_name = match.group(1)
            value = getenv(variable_name)

            if value is None:
                raise ConfigEnvironmentVariableError(
                    f"Required environment variable is not set: {variable_name}"
                )

            return value

        return _ENV_VAR_PATTERN.sub(replace, content)
