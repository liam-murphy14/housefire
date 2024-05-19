import os


def get_env_nonnull(key: str) -> str:
    """Get an environment variable and raise an error if it is None."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is not set.")
    return value


def get_env_nonnull_path(key: str) -> str:
    """Get an environment variable and raise an error if it is None or does not exist."""
    value = get_env_nonnull(key)
    if not os.path.exists(value):
        raise ValueError(f"Path {value} does not exist.")
    return value


def get_env_nonnull_file(key: str) -> str:
    """Get an environment variable and raise an error if it is None or does not exist."""
    value = get_env_nonnull(key)
    if not os.path.isfile(value):
        raise ValueError(f"File {value} does not exist.")
    return value


def get_env_nonnull_dir(key: str) -> str:
    """Get an environment variable and raise an error if it is None or does not exist."""
    value = get_env_nonnull(key)
    if not os.path.isdir(value):
        raise ValueError(f"Directory {value} does not exist.")
    return value
