from pathlib import Path

from loguru import logger

_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <5}</level> | "
    "<cyan>[{extra[service]: <10}]</cyan> | "
    "<blue>{name}:{function}:{line}</blue>\n"
    "<level>| {message}</level>"
)


def configure_logging(
    service: str,
    *,
    log_directory: str | Path = "logs",
) -> None:
    """Configure application logging for a service.

    Args:
        service: Name identifying the application or service.
        log_directory: Root directory used for log files.
    """
    if not service.strip():
        raise ValueError("Service name cannot be empty.")

    log_path = Path(log_directory) / service
    log_path.mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.configure(
        extra={"service": service.upper()},
    )

    logger.add(
        sink=lambda message: print(message, end=""),
        format=_LOG_FORMAT,
        level="DEBUG",
        colorize=True,
    )

    logger.add(
        log_path / "{time:YYYY-MM-DD}.log",
        format=_LOG_FORMAT,
        level="DEBUG",
        rotation="00:00",
        retention="30 days",
        encoding="utf-8",
    )