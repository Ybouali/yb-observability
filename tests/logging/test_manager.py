from collections.abc import Generator
from pathlib import Path

import pytest
from loguru import logger

from yb_observability.logging import configure_logging


@pytest.fixture(autouse=True)
def reset_logger() -> Generator[None]:
    logger.remove()
    yield
    logger.remove()


class TestConfigureLogging:
    def test_creates_service_log_directory(
        self,
        tmp_path: Path,
    ) -> None:
        configure_logging(
            service="backend",
            log_directory=tmp_path,
        )

        assert (tmp_path / "backend").is_dir()

    def test_creates_log_file(
        self,
        tmp_path: Path,
    ) -> None:
        configure_logging(
            service="backend",
            log_directory=tmp_path,
        )

        logger.info("Test log message")

        log_files = list((tmp_path / "backend").glob("*.log"))

        assert len(log_files) == 1
        assert "Test log message" in log_files[0].read_text(encoding="utf-8")

    def test_uses_service_name_in_log_output(
        self,
        tmp_path: Path,
    ) -> None:
        configure_logging(
            service="backend",
            log_directory=tmp_path,
        )

        logger.info("Service test")

        log_file = next((tmp_path / "backend").glob("*.log"))
        content = log_file.read_text(encoding="utf-8")

        assert "[BACKEND" in content
        assert "Service test" in content

    def test_supports_custom_log_directory(
        self,
        tmp_path: Path,
    ) -> None:
        custom_directory = tmp_path / "application-logs"

        configure_logging(
            service="worker",
            log_directory=custom_directory,
        )

        logger.info("Custom directory test")

        log_files = list((custom_directory / "worker").glob("*.log"))

        assert len(log_files) == 1

    def test_normalizes_service_name_in_output(
        self,
        tmp_path: Path,
    ) -> None:
        configure_logging(
            service="backend",
            log_directory=tmp_path,
        )

        logger.info("Normalization test")

        log_file = next((tmp_path / "backend").glob("*.log"))
        content = log_file.read_text(encoding="utf-8")

        assert "[BACKEND" in content

    def test_rejects_empty_service_name(
        self,
        tmp_path: Path,
    ) -> None:
        with pytest.raises(
            ValueError,
            match="Service name cannot be empty",
        ):
            configure_logging(
                service="",
                log_directory=tmp_path,
            )

    def test_rejects_whitespace_service_name(
        self,
        tmp_path: Path,
    ) -> None:
        with pytest.raises(
            ValueError,
            match="Service name cannot be empty",
        ):
            configure_logging(
                service="   ",
                log_directory=tmp_path,
            )

    def test_reconfiguring_does_not_duplicate_handlers(
        self,
        tmp_path: Path,
    ) -> None:
        configure_logging(
            service="backend",
            log_directory=tmp_path,
        )

        configure_logging(
            service="backend",
            log_directory=tmp_path,
        )

        logger.info("Single configuration test")

        log_file = next((tmp_path / "backend").glob("*.log"))
        content = log_file.read_text(encoding="utf-8")

        assert content.count("Single configuration test") == 1

    def test_supports_path_object(
        self,
        tmp_path: Path,
    ) -> None:
        log_directory = Path(tmp_path)

        configure_logging(
            service="ai",
            log_directory=log_directory,
        )

        logger.info("Path test")

        assert (log_directory / "ai").is_dir()


def test_logger_public_import() -> None:
    from yb_observability.logging import logger as public_logger

    assert public_logger is logger


def test_logger_manager_import_remains_compatible() -> None:
    from yb_observability.logging import logger as public_logger
    from yb_observability.logging.manager import logger as manager_logger

    assert public_logger is manager_logger


def test_logging_public_api() -> None:
    from yb_observability.logging import (
        configure_logging as public_configure_logging,
    )
    from yb_observability.logging import logger as public_logger

    assert public_configure_logging is configure_logging
    assert public_logger is logger
