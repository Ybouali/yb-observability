class ConfigLoaderError(Exception):
    """Base exception for configuration loading errors."""


class ConfigFileNotFoundError(ConfigLoaderError):
    """Raised when the configuration file cannot be found."""


class ConfigEnvironmentVariableError(ConfigLoaderError):
    """Raised when a required environment variable is missing."""
