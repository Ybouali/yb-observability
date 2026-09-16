from __future__ import annotations

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

# ${VAR} or ${VAR:-default}
_ENV_VAR_PATTERN = compile(
    r"\$\{(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?::-?(?P<default>[^}]*))?\}"
)
# $$  -> escape for a literal $ (so `$${VAR}` renders as `${VAR}`)
_ESCAPE = "\x00yb-escape\x00"


class ConfigLoader:
    """Load YAML configuration and resolve environment variables."""

    def __init__(self, config_path: str | Path) -> None:
        self.config_path = Path(config_path)

    def load(self) -> dict[str, Any]:
        """Load the configuration file and resolve `${VAR}` references."""

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

        try:
            raw = safe_load(content)
        except YAMLError as exc:
            raise ConfigLoaderError(
                f"Invalid YAML configuration: {self.config_path}"
            ) from exc

        if raw is None:
            return {}

        if not isinstance(raw, dict):
            raise ConfigLoaderError(
                "The root of the configuration file must be a YAML mapping."
            )

        return self._resolve_node(raw)

    # ---- internals -----------------------------------------------------

    def _resolve_node(self, node: Any) -> Any:
        """Recursively resolve `${VAR}` inside string leaves."""
        if isinstance(node, str):
            return self._resolve_string(node)
        if isinstance(node, dict):
            return {key: self._resolve_node(value) for key, value in node.items()}
        if isinstance(node, list):
            return [self._resolve_node(item) for item in node]
        return node

    @staticmethod
    def _resolve_string(value: str) -> str:
        if "${" not in value and "$$" not in value:
            return value

        # Protect `$$` so it survives env substitution and becomes `$`.
        protected = value.replace("$$", _ESCAPE)

        def replace(match: Match[str]) -> str:
            name = match.group("name")
            default = match.group("default")

            env_value = getenv(name)
            if env_value is not None:
                return env_value
            if default is not None:
                return default

            raise ConfigEnvironmentVariableError(
                f"Required environment variable is not set: {name}"
            )

        resolved = _ENV_VAR_PATTERN.sub(replace, protected)
        return resolved.replace(_ESCAPE, "$")
