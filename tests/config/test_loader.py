from pathlib import Path

import pytest

from yb_observability.config.exceptions import (
    ConfigEnvironmentVariableError,
    ConfigFileNotFoundError,
    ConfigLoaderError,
)
from yb_observability.config.loader import ConfigLoader


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent / "fixtures"


class TestConfigLoader:
    def test_load_valid_configuration(self, fixtures_path: Path) -> None:
        config_path = fixtures_path / "valid.yml"

        loader = ConfigLoader(config_path)  # noqa: F821

        config = loader.load()

        assert config == {
            "application": {
                "name": "Example Application",
                "environment": "development",
                "debug": True,
                "version": "0.1.0",
            },
            "database": {
                "host": "localhost",
                "port": 5432,
            },
        }

    def test_load_resolves_environment_variables(
        self,
        fixtures_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_path = fixtures_path / "environment.yml"

        monkeypatch.setenv("APP_NAME", "Example Application")
        monkeypatch.setenv("ENVIRONMENT", "development")

        loader = ConfigLoader(config_path)

        config = loader.load()

        assert config == {
            "application": {
                "name": "Example Application",
                "environment": "development",
            }
        }

    def test_load_resolves_nested_environment_variables(
        self,
        fixtures_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_path = fixtures_path / "nested_environment.yml"

        monkeypatch.setenv("POSTGRES_HOST", "postgres")
        monkeypatch.setenv("POSTGRES_USER", "example_user")

        loader = ConfigLoader(config_path)

        config = loader.load()

        assert config == {
            "database": {
                "host": "postgres",
                "credentials": {
                    "user": "example_user",
                },
            }
        }

    def test_load_raises_when_config_file_does_not_exist(
        self,
        tmp_path: Path,
    ) -> None:
        config_path = tmp_path / "missing.yml"

        loader = ConfigLoader(config_path)

        with pytest.raises(
            ConfigFileNotFoundError,
            match="Configuration file not found",
        ):
            loader.load()

    def test_load_raises_when_config_file_cannot_be_read(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_path = tmp_path / "config.yml"
        config_path.write_text("application: {}", encoding="utf-8")

        def raise_os_error(*args: object, **kwargs: object) -> str:
            raise OSError("permission denied")

        monkeypatch.setattr(Path, "read_text", raise_os_error)

        loader = ConfigLoader(config_path)

        with pytest.raises(
            ConfigLoaderError,
            match="Unable to read configuration file",
        ):
            loader.load()

    def test_load_raises_when_yaml_is_invalid(
        self,
        fixtures_path: Path,
    ) -> None:
        config_path = fixtures_path / "invalid.yml"

        loader = ConfigLoader(config_path)

        with pytest.raises(
            ConfigLoaderError,
            match="Invalid YAML configuration",
        ):
            loader.load()

    def test_load_raises_when_environment_variable_is_missing(
        self,
        fixtures_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        config_path = fixtures_path / "environment.yml"

        monkeypatch.delenv("APP_NAME", raising=False)

        with pytest.raises(
            ConfigEnvironmentVariableError,
            match="Required environment variable is not set: APP_NAME",
        ):
            ConfigLoader(config_path).load()

    def test_load_returns_empty_dict_for_empty_yaml(
        self,
        tmp_path: Path,
    ) -> None:
        config_path = tmp_path / "empty.yml"
        config_path.write_text("", encoding="utf-8")

        loader = ConfigLoader(config_path)

        assert loader.load() == {}

    def test_load_raises_when_yaml_root_is_not_mapping(
        self,
        fixtures_path: Path,
    ) -> None:
        config_path = fixtures_path / "scalar.yml"

        loader = ConfigLoader(config_path)

        with pytest.raises(
            ConfigLoaderError,
            match="root of the configuration file must be a YAML mapping",
        ):
            loader.load()
